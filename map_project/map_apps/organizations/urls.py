from django.urls import include, path

from .views import OrganizationCreateAPIView

app_name = 'organizations'

urlpatterns = [
    path('organization-create/', OrganizationCreateAPIView.as_view(), name='organization-create'),
]
