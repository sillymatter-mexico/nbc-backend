from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from users.controllers import ClientUserControllers


class DefaultResponse(object):
    @classmethod
    def api_response(cls, data, status=200):
        response = HttpResponse(data, content_type='application/json')
        response.status_code = status
        return Response(data, status=status)

    @classmethod
    def api_ok_response(cls, data, messages, status_code=200):
        response = dict(
            success=True,
            messages=messages,
            data=data,
            datetime=timezone.now().strftime('%Y-%m-%d %H:%M:%SZ')
        )
        return cls.api_response(response, status_code)

    @classmethod
    def api_fail_response(cls, data, messages, status_code=400):
        response = dict(
            success=False,
            messages=messages,
            data=data,
            datetime=timezone.now().strftime('%Y-%m-%d %H:%M:%SZ')
        )
        return cls.api_response(response, status_code)


class NoTokenView(APIView, DefaultResponse):
    pass


class TokenView(APIView, DefaultResponse):
    user = None
    user_required = True

    def get_auth_token_from_headers(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return None
        return request.META['HTTP_AUTHORIZATION']
    def dispatch(self, request, *args, **kwargs):
        token = self.get_auth_token_from_headers(request)
        if token is None:
            response = self.api_fail_response(None, 'Se requiere token')
            return JsonResponse(response.data, status=401)
        data = ClientUserControllers.get_by_token(token)
        if data is None:
            response = self.api_fail_response(None, 'Token incorrecto')
            return JsonResponse(response.data, status=401)
        self.user = ClientUserControllers.get_by_uuid(data['uuid'])
        response = super(TokenView, self).dispatch(request, *args, **kwargs)
        return response