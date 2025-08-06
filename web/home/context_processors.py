from auth.models import UserProfile


def user_role(request):
    """
    Context processor to add user role to all templates
    """
    context = {
        'user_role': None,
    }
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            context['user_role'] = user_profile.role
        except UserProfile.DoesNotExist:
            context['user_role'] = None
    
    return context
