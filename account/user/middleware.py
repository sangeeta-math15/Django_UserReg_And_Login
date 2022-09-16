from user.models import UserLogs
import logging

logging.basicConfig(filename="view.log", level=logging.INFO, filemode="w", force=True)


class DemoMiddleware:

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        return response

    # middleware hook
    def process_view(self, request, view_func, view_args, view_kwargs):
        UserLogs.objects.create(request_method=request.method, request_url=request.path)
