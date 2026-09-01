from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, SkillMatch


class SkillSwapAPITestCase(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='TestPassword123!'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='TestPassword123!'
        )

        refresh = RefreshToken.for_user(
            self.user1
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f'Bearer {refresh.access_token}'
            )
        )

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    def test_unauthenticated_profile_access(self):

        self.client.credentials()

        response = self.client.get(
            '/api/profiles/'
        )

        self.assertEqual(
            response.status_code,
            401
        )

    # ========================================================
    # PROFILE CRUD
    # ========================================================

    def test_create_profile(self):

        response = self.client.post(
            '/api/profiles/',
            {
                'bio': 'Backend developer',
                'skills_have': 'Python, Django',
                'skills_want': 'React'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            UserProfile.objects.filter(
                user=self.user1
            ).exists()
        )

    def test_list_profile(self):

        UserProfile.objects.create(
            user=self.user1,
            bio='Developer',
            skills_have='Python',
            skills_want='React'
        )

        response = self.client.get(
            '/api/profiles/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_update_profile(self):

        profile = UserProfile.objects.create(
            user=self.user1,
            bio='Old bio',
            skills_have='Python',
            skills_want='React'
        )

        response = self.client.patch(
            f'/api/profiles/{profile.id}/',
            {
                'bio': 'Updated bio'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_delete_profile(self):

        profile = UserProfile.objects.create(
            user=self.user1,
            bio='Developer',
            skills_have='Python',
            skills_want='React'
        )

        response = self.client.delete(
            f'/api/profiles/{profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            204
        )

    # ========================================================
    # SKILL MATCH
    # ========================================================

    def test_create_skill_match(self):

        response = self.client.post(
            '/api/skill-matches/',
            {
                'receiver_id': self.user2.id,
                'skill': 'Python'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            SkillMatch.objects.filter(
                sender=self.user1,
                receiver=self.user2,
                skill='Python'
            ).exists()
        )

    def test_cannot_match_self(self):

        response = self.client.post(
            '/api/skill-matches/',
            {
                'receiver_id': self.user1.id,
                'skill': 'Python'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_skill_validation(self):

        response = self.client.post(
            '/api/skill-matches/',
            {
                'receiver_id': self.user2.id,
                'skill': ''
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_skill_match_list(self):

        SkillMatch.objects.create(
            sender=self.user1,
            receiver=self.user2,
            skill='Python'
        )

        response = self.client.get(
            '/api/skill-matches/'
        )

        self.assertEqual(
            response.status_code,
            200
        )