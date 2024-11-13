import django.urls

from .views import SignUpView

urlpatterns = [
    django.urls.path('signup/', SignUpView.as_view(), name='signup'),
]
