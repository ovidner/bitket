from csv import DictReader

from django.core.validators import validate_email
from django.db import transaction

from bitket import models
from bitket.fields import LIU_ID

event = models.Event.objects.get(name='Luciafesten 2017')

ticket_type_party = event.ticket_types.get(name='Party ticket')
ticket_type_banquet = event.ticket_types.get(name='Christmas banquet + Party ticket')

variation_choice_beverage_beer = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Beer')
variation_choice_beverage_cider = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Cider')
variation_choice_beverage_non_alco = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Non-alcoholic')
variation_choice_food_na = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='No special requests')
variation_choice_food_vegetarian = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Vegetarian')
variation_choice_food_vegan = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Vegan')
variation_choice_food_gluten_free = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Gluten free')
variation_choice_food_lactose_free = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='Lactose free')
variation_choice_food_special = models.VariationChoice.objects.get(variation__ticket_type=ticket_type_banquet, name='I will send my requests to food@litheblas.org')


def _get_ticket_type_and_variation_choices(row):
    ticket_beverage_text = row['Biljett']
    food_text = row['Matpreferens (Om din vän ska på sittningen)']
    if ticket_beverage_text.startswith('Sittningsbiljett'):
        if 'Öl' in ticket_beverage_text:
            beverage_choice = variation_choice_beverage_beer
        elif 'Cider' in ticket_beverage_text:
            beverage_choice = variation_choice_beverage_cider
        elif 'Alkoholfri' in ticket_beverage_text:
            beverage_choice = variation_choice_beverage_non_alco
        food_choice = {
            '': variation_choice_food_na,
            'Vegetarian': variation_choice_food_vegetarian,
            'Vegan': variation_choice_food_vegan,
            'Laktosintollerant': variation_choice_food_lactose_free,
            'Glutenintollerant': variation_choice_food_gluten_free,
            'Mer specifik specialkost. Din vän skickar ett mejl till food@litheblas.org': variation_choice_food_special,
        }[food_text]

        return (ticket_type_banquet, [beverage_choice, food_choice])

    elif ticket_beverage_text.startswith('Luciafest'):
        return (ticket_type_party, [])


def _get_or_create_user(row):
    email_or_liu_id = row['LiU-ID eller mejl till den som ska ha biljetten'].strip().lower()
    name = row['Namn på den som ska ha biljetten'].strip()

    if LIU_ID.match(email_or_liu_id):
        liu_id = email_or_liu_id
    elif email_or_liu_id.endswith('@student.liu.se'):
        liu_id = email_or_liu_id.split('@')[0]
    else:
        liu_id = None
        validate_email(email_or_liu_id)

    if liu_id:
        sesam_student = models.sesam_student_service_client.get_student(liu_id=liu_id)
        union = (
            models.StudentUnion.objects.get(name=sesam_student.main_union)
            if sesam_student.main_union else None
        )
        name = sesam_student.full_name
        email = sesam_student.email
    else:
        union = None
        email = email_or_liu_id

    try:
        user = models.User.objects.get(email__iexact=email)
    except models.User.DoesNotExist:
        user = models.User.objects.create(email=email, name=name)
        user.set_password(None)

    user.student_union = union
    user.save()

    return user


def import_tsv(filename):
    ticket_ownerships = []
    with transaction.atomic():
        with open(filename, encoding='utf-8') as f:
            reader = DictReader(f, dialect='excel-tab')

            for row in reader:
                if row['Fel'] or row['Bitket-ID']:
                    print(',')
                    continue
                user = _get_or_create_user(row)
                ticket_type, variation_choices = _get_ticket_type_and_variation_choices(row)
                ticket = models.Ticket.objects.create(
                    ticket_type=ticket_type,
                    pending=False,
                )
                ticket.variation_choices.set(variation_choices)
                ticket.save()

                ticket_ownership = models.TicketOwnership.objects.create(
                    ticket=ticket,
                    user=user,
                )

                ticket_ownership.transactions.set([
                    models.Transaction.objects.create(
                        amount=ticket_ownership.price,
                    )
                ])

                ticket_ownerships.append(ticket_ownership)

                print(int(ticket_ownership.price), str(ticket.pk), sep=',')

    for to in ticket_ownerships:
        to.email_confirmation()
