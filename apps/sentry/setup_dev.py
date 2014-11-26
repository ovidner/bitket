# -*- coding: utf-8 -*-

# From http://sentry.readthedocs.org/en/latest/faq/index.html#how-do-i

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
from sentry.models import User, Team, TeamMember, Project, ProjectKey

try:
    admin = User()
    admin.username = 'admin'
    admin.email = 'it@sof15.se'
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password('bajsmacka')
    admin.save()
except:
    pass

try:
    sof15_team = Team()
    sof15_team.slug = 'sof15'
    sof15_team.name = 'SOF15'
    sof15_team.owner = User.objects.get(username='admin')
    sof15_team.save()
except:
    pass

try:
    admin_sof15_teammember = TeamMember()
    admin_sof15_teammember.team = Team.objects.get(slug='sof15')
    admin_sof15_teammember.user = User.objects.get(username='admin')
    admin_sof15_teammember.type = 0
    admin_sof15_teammember.save()
except:
    pass

try:
    sof15_project = Project()
    sof15_project.slug = 'sof15'
    sof15_project.name = 'SOF15'
    sof15_project.team = Team.objects.get(slug='sof15')
    sof15_project.platform = 'django'
    sof15_project.save()
except:
    pass

try:
    sof15_project_key = ProjectKey()
    sof15_project_key.project = Project.objects.get(slug='sof15')
    sof15_project_key.public_key = '84863b989a8b43408184cc6074004fa2'
    sof15_project_key.secret_key = 'd26e02ebdee549d7ac6aa3b42f83d5d2'
    sof15_project_key.save()
except:
    pass