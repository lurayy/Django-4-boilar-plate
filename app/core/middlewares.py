from django.core.cache import cache


def get_user(token):
    data = cache.get('user_' + token)
    return data


class APIAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = request.headers.get('Authorization', None)
        if key:
            data = get_user(request.headers['Authorization'])
            if data:
                request.user = data['user']
        response = self.get_response(request)
        return response


class DisableCSRF(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)

        return response
