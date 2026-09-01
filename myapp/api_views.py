from django.contrib.auth.models import User
from django_q.tasks import async_task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile, SkillMatch

from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdmin

from .serializers import (
    UserProfileSerializer,
    SkillMatchSerializer,
)   

class AdminUserViewSet(viewsets.ViewSet):

    permission_classes = [IsAdmin]

    @action(
        detail=False,
        methods=['get'],
        url_path='users'
    )
    def users(self, request):

        users = User.objects.all().values(
            'id',
            'username',
            'email',
            'is_active'
        )

        return Response({
            'count': users.count(),
            'users': list(users)
        })


# ============================================================
# USER PROFILE API
# ============================================================

class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return UserProfile.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        if UserProfile.objects.filter(
            user=self.request.user
        ).exists():

            raise ValidationError({
                'detail':
                    'You already have a profile. '
                    'Use PUT or PATCH to update it.'
            })

        serializer.save(
            user=self.request.user
        )


# ============================================================
# SKILL MATCH API
# ============================================================

class SkillMatchViewSet(viewsets.ModelViewSet):

    serializer_class = SkillMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return SkillMatch.objects.filter(
            sender=self.request.user
        ) | SkillMatch.objects.filter(
            receiver=self.request.user
        )

    def perform_create(self, serializer):

        receiver = serializer.validated_data.get(
            'receiver'
        )

        if receiver is None:

            raise ValidationError({
                'receiver_id':
                    'Receiver is required.'
            })

        if receiver == self.request.user:

            raise ValidationError({
                'receiver_id':
                    'You cannot send a skill match '
                    'to yourself.'
            })

        if SkillMatch.objects.filter(
            sender=self.request.user,
            receiver=receiver,
            skill=serializer.validated_data['skill']
        ).exists():

            raise ValidationError({
                'skill':
                    'This skill match already exists.'
            })

        serializer.save(
            sender=self.request.user,
            receiver=receiver
        )
class AsyncMatchViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['post'],
        url_path='process'
    )
    def process(self, request, pk=None):

        task_id = async_task(
            'myapp.tasks.process_skill_match',
            pk
        )

        return Response(
            {
                'message': 'Skill match processing started asynchronously.',
                'task_id': task_id,
                'match_id': pk
            },
            status=status.HTTP_202_ACCEPTED
        )
