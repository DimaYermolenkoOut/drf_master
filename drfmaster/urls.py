"""
URL configuration for drfmaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import LogoutView
from django.contrib import admin

from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view

from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from drfcalendar.filters import BookingFilter
from drfcalendar.viewsets import slots, BookingViewSet, slots_view, ServiceViewSet, \
    MasterScheduleViewSet
from .schema import schema

router = DefaultRouter()
router.register('bookings', BookingViewSet)
router.register('services', ServiceViewSet)
router.register('masterschedules', MasterScheduleViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="drfmaster API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.drfmaster.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path("", TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('allauth.urls')),
    path("logout", LogoutView.as_view()),

    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path("slots/<int:master_id>/<int:service_id>/<str:date>/", slots),
    path('slots/<int:master_id>/<int:service_id>/', slots_view),
    path('api/', include(router.urls)),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
    # path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
