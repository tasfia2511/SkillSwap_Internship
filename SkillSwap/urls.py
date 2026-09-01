"""
URL configuration for SkillSwap project.
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # ========================================================
    # ADMIN
    # ========================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # ========================================================
    # DJANGO ALLAUTH
    #
    # Used for Google/social authentication.
    #
    # Normal SkillSwap login/signup/logout are handled by
    # myapp.urls.
    # ========================================================

    path(
        'accounts/',
        include('allauth.urls')
    ),


    # ========================================================
    # SKILLSWAP WEB APPLICATION
    # ========================================================

    path(
        '',
        include('myapp.urls')
    ),


    # ========================================================
    # REST API
    # ========================================================

    path(
        'api/',
        include('myapp.api_urls')
    ),


    # ========================================================
    # JWT AUTHENTICATION
    # ========================================================

    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]