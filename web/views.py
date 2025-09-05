from django.shortcuts import render
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'home/home.html')

class DRFLoginView(LoginView):
    template_name = "rest_framework/login.html"

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.get_form(),
            'next': request.GET.get('next', ''),
            'name': 'Login',
            'code_style': 'friendly',
        }
        return render(request, self.template_name, context)
