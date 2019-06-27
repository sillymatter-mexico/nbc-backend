from django import http


class CORSMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_response(self, request, response):
        response.setdefault('Access-Control-Allow-Origin', '*')
        response.setdefault('Access-Control-Allow-Headers', 'Authorization')
        response.setdefault('Access-Control-Request-Method', 'GET, POST, PUT, DELETE, OPTIONS')

        # Inject cookie if session was detected in view
        if hasattr(request, 'api_token_key') and hasattr(request, 'api_token'):
            response.set_cookie(request.api_token_key, request.api_token)

        return response


    def process_request(self, request):
        if request.method == 'OPTIONS' and \
                        'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:

            response = http.HttpResponse()
            response.setdefault('Access-Control-Allow-Origin', '*')
            response.setdefault('Access-Control-Allow-Headers',
                                'Access-Control-Allow-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Content-Type,Authorization')
            response.setdefault('Access-Control-Request-Method',
                                'GET, POST, PUT, DELETE, OPTIONS')
            response.setdefault('Access-Control-Allow-Methods',
                                'GET, POST, PUT, DELETE, OPTIONS')
            return response