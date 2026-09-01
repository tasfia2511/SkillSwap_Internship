from django.contrib.auth.models import User
from django.utils import timezone


def process_skill_match(match_id):
    from .models import SkillMatch

    try:
        match = SkillMatch.objects.get(id=match_id)

        print(
            f"[{timezone.now()}] "
            f"Processing SkillMatch {match.id}: "
            f"{match.sender.username} -> "
            f"{match.receiver.username}"
        )

        return {
            "match_id": match.id,
            "status": "processed",
        }

    except SkillMatch.DoesNotExist:
        return {
            "match_id": match_id,
            "status": "not_found",
        }