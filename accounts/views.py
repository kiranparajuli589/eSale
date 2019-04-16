from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import User, UserProfile, Log


def register(request, *args, **kwargs):
    title = 'User Registration'
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        Log.objects.create(user=user.get_full_name(), subject='Registration', detail='User Registration Complete')
        return redirect('login')
    context = {
        'title': title,
        'form': form
    }
    return render(request, "accounts/register.html", context)


@login_required
def profile(request):
    title = 'User Profile'
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        context = {
            'user': user,
            'title': title
        }
        return render(request, 'dashboard/profile.html', context)
    except:
        profile = UserProfile.objects.create(user=user)
        context = {
            'user': user,
            'title': title
        }
        return render(request, 'dashboard/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': u_form,
        'profile_form': p_form
    }

    return render(request, 'dashboard/edit_profile.html', context)
