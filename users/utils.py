from users.models import User, UserSettings
from django.contrib.auth.hashers import get_hasher, identify_hasher


def get_or_create_user_settings(user, **kwargs):
    user = User.objects.get(id=user.id)

    if user is None:
        raise ValueError("user is required")

    preferred_hash_algorithm = kwargs.get("algorithm", "pbkdf2_sha256")

    try:
        user_settings = UserSettings.objects.get(user=user)
    except UserSettings.DoesNotExist:
        user_settings = UserSettings.objects.create(
            user=user, 
            preferred_hash_algorithm=preferred_hash_algorithm
        )

    return user_settings


def update_password():
    ...

def check_password(password, encoded, hasher):
    if password is None:
        return False, False
    
    preferred_hasher = get_hasher(hasher)
    try:
        used_hasher = identify_hasher(encoded)
    except ValueError:
        return False, False
    
    hasher_changed = preferred_hasher != used_hasher
    is_correct = used_hasher.verify(password, encoded)

    return is_correct, hasher_changed
    
