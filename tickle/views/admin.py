# -*- coding: utf-8 -*-
from django.views.generic import FormView, CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


from tickle.models import Holding, Person
from tickle.forms import AddProductToShoppingCartForm


class AddProductToShoppingCartAdminView(CreateView):
    model = Holding
    form_class = AddProductToShoppingCartForm
    template_name = 'admin/tickle/person/add_product_to_shopping_cart.html'

    def get_success_url(self):
        messages.success(self.request, _('Added product to shopping cart(s).'))
        return reverse('admin:tickle_person_changelist')

    def get_initial(self):
        return {'people': self.get_people()}

    def get_people(self):
        selected = self.request.GET.get('ids')

        return Person.objects.filter(pk__in=selected.split(','))

    def get_context_data(self, **kwargs):
        context = super(AddProductToShoppingCartAdminView, self).get_context_data(**kwargs)

        context['content_type'] = self.model._meta.verbose_name_plural.title()

        return context
