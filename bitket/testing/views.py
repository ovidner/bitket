import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, View


class FakeAuthorizationView(View):
    def get(self, request, *args, **kwargs):
        # http://localhost:53791/__test__/auth/facebook/authorization/?client_id=6ed549a3-d50f-45f3-93ac-f510eede3ae5&code=abc%3Fresponse_type%3Dcode&redirect_uri=http%3A%2F%2Flocalhost%3A53791%2Flog-in%2Fliu%2F&resource=https%3A%2F%2Fwww.bitket.se&state=%2Freprehenderit%2F
        return TemplateResponse(request, 'testing/fake_authorization_view.html', context=dict(
            kwargs=kwargs,
            get_params=request.GET,
        ))

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        key = kwargs['key']
        redirect_uri = request.POST['redirect_uri']
        state = request.POST['state']
        if action == 'succeed':
            return HttpResponseRedirect(f'{redirect_uri}?code={key}&state={state}')
        elif action == 'fail':
            return HttpResponseRedirect()


class FakeTokenView(View):
    def post(self, request, *args, **kwargs):
        print('bam!')
        return HttpResponse(json.dumps(dict(
            access_token='',
            token_type='bearer',
            expires_in=3600
        )))
