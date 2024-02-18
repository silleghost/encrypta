from users.models import User, UserSettings


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
