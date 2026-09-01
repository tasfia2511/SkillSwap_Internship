from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('USER', 'User'),
        ('MODERATOR', 'Moderator'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    bio = models.TextField(blank=True)

    skills_have = models.CharField(
        max_length=255,
        blank=True
    )

    skills_want = models.CharField(
        max_length=255,
        blank=True
    )

    verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username

class SkillMatch(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_matches'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_matches'
    )

    skill = models.CharField(
        max_length=100
    )

    accepted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver', 'skill'],
                name='unique_skill_match'
            )
        ]

    def __str__(self):
        return (
            f"{self.sender.username} → "
            f"{self.receiver.username} "
            f"({self.skill})"
        )