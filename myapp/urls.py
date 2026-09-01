from django.urls import path
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter
from .api_views import (
    UserProfileViewSet,
    SkillMatchViewSet,
    AdminUserViewSet,
)

from . import views
from .api_views import (
    UserProfileViewSet,
    SkillMatchViewSet,
)


# ============================================================
# REST API ROUTER
# ============================================================

router = DefaultRouter()

router.register(
    r'api/profiles',
    UserProfileViewSet,
    basename='profile'
)

router.register(
    r'api/skill-matches',
    SkillMatchViewSet,
    basename='skill-match'
)
router.register(
    r'admin',
    AdminUserViewSet,
    basename='admin'
)

urlpatterns = [

    # ========================================================
    # PUBLIC PAGES
    # ========================================================

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'services/',
        views.services,
        name='services'
    ),

    path(
        'services/<slug:category>/',
        views.service_detail,
        name='service_detail'
    ),

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='home'
        ),
        name='logout'
    ),

    # ========================================================
    # PROFILE
    # ========================================================

    path(
        'profile/create/',
        views.create_profile,
        name='create_profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    # ========================================================
    # MATCHING
    # ========================================================

    path(
        'find-matches/',
        views.find_matches,
        name='find_matches'
    ),

    path(
        'match-list/',
        views.match_list,
        name='match_list'
    ),

    path(
        'match/send/<int:user_id>/',
        views.send_match_request,
        name='send_match_request'
    ),

    path(
        'match/<int:match_id>/accept/',
        views.accept_match,
        name='accept_match'
    ),

    path(
        'match/<int:match_id>/reject/',
        views.reject_match,
        name='reject_match'
    ),

    # ========================================================
    # EXISTING API
    # ========================================================

    path(
        'api/profile/create/',
        views.create_profile_api,
        name='create_profile_api'
    ),

    path(
        'api/profile/update/',
        views.update_profile_api,
        name='update_profile_api'
    ),

    path(
        'api/profile/delete/',
        views.delete_profile_api,
        name='delete_profile_api'
    ),
]


# ============================================================
# REST API ROUTER URLS
# ============================================================

urlpatterns += router.urls