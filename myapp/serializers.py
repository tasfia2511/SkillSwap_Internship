from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile, SkillMatch


# ============================================================
# USER SERIALIZER
# ============================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]

        read_only_fields = [
            'id',
        ]


# ============================================================
# USER PROFILE SERIALIZER
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        read_only=True
    )

    class Meta:
        model = UserProfile

        fields = [
            'id',
            'user',
            'bio',
            'skills_have',
            'skills_want',
        ]

        read_only_fields = [
            'id',
            'user',
        ]

    # --------------------------------------------------------
    # VALIDATE SKILLS HAVE
    # --------------------------------------------------------

    def validate_skills_have(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Please provide at least one skill you can teach.'
            )

        return value

    # --------------------------------------------------------
    # VALIDATE SKILLS WANT
    # --------------------------------------------------------

    def validate_skills_want(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Please provide at least one skill you want to learn.'
            )

        return value

    # --------------------------------------------------------
    # VALIDATE BIO
    # --------------------------------------------------------

    def validate_bio(self, value):

        value = value.strip()

        if len(value) > 1000:
            raise serializers.ValidationError(
                'Bio cannot contain more than 1000 characters.'
            )

        return value

    # --------------------------------------------------------
    # CREATE PROFILE
    # --------------------------------------------------------

    def create(self, validated_data):

        request = self.context.get(
            'request'
        )

        if request is None:
            raise serializers.ValidationError(
                'Request context is required.'
            )

        user = request.user

        profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )

        return profile

    # --------------------------------------------------------
    # UPDATE PROFILE
    # --------------------------------------------------------

    def update(self, instance, validated_data):

        instance.bio = validated_data.get(
            'bio',
            instance.bio
        )

        instance.skills_have = validated_data.get(
            'skills_have',
            instance.skills_have
        )

        instance.skills_want = validated_data.get(
            'skills_want',
            instance.skills_want
        )

        instance.save()

        return instance


# ============================================================
# SKILL MATCH SERIALIZER
# ============================================================

class SkillMatchSerializer(serializers.ModelSerializer):

    sender = UserSerializer(
        read_only=True
    )

    receiver = UserSerializer(
        read_only=True
    )

    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='receiver',
        write_only=True
    )

    class Meta:
        model = SkillMatch

        fields = [
            'id',
            'sender',
            'receiver',
            'receiver_id',
            'skill',
            'accepted',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'sender',
            'receiver',
            'accepted',
            'created_at',
        ]

    def validate_skill(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Skill cannot be empty.'
            )

        if len(value) > 100:
            raise serializers.ValidationError(
                'Skill name cannot exceed 100 characters.'
            )

        return value