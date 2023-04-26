from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class TemplateLoginView(TemplateView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(TemplateLoginView, self).dispatch(*args, **kwargs)

