from django.shortcuts import redirect

class NormalizeDoubleSlashMiddleware:
    """
    Middleware to normalize double slashes in URLs like //api/error -> /api/error
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '//' in request.path:
            fixed_path = request.path.replace('//', '/')
            if fixed_path != request.path:
                return redirect(fixed_path, permanent=True)
        return self.get_response(request)