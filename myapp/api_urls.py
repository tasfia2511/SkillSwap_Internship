from rest_framework.routers import DefaultRouter

from .api_views import (
    UserProfileViewSet,
    SkillMatchViewSet,
    AsyncMatchViewSet
)

router = DefaultRouter()

router.register(
    r'profiles',
    UserProfileViewSet,
    basename='profile'
)

router.register(
    r'matches',
    SkillMatchViewSet,
    basename='match'
)

router.register(
    r'async-matches',
    AsyncMatchViewSet,
    basename='async-match'
)

urlpatterns = router.urls