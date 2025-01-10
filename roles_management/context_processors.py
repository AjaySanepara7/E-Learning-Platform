from django.contrib.auth.models import User


def user_profile_object(request):
    if request.user.is_authenticated:
        profile = request.user.profile_set.first()
        return {"user_profile": profile}
    return {}