from django.shortcuts import render
from django.contrib.auth.models import User 
from accounts.models import UserProfile

# Create your views here.

def profile_detail(request, current_user_id):

    current_user = User.objects.get(id = current_user_id)

    tmp = 'light_template.html'

    if request.user.is_authenticated:

        profile_theme = UserProfile.objects.get(user_id = request.user.id).theme

        if profile_theme == 'd':
            tmp = 'dark_template.html'

    return render(
        request,
        'accounts/profile.html',
        context = {
            'tmp'   : tmp,
            'current_user'  : current_user,
        }
    )