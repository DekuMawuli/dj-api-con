from functools import wraps
from django.shortcuts import redirect


def user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'email' not in request.session:
            return redirect('system:login_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_not_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'email' in request.session:
            return redirect('system:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
