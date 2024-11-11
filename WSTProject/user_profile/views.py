from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def view_profile(request):
    return render(request, 'profile/view_profile.html', {
        'title': 'Profile',
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            gender = request.POST['gender']
            image = request.FILES.get('image')

            #Profile Model
            if image:
                request.user.profile.image = image
            request.user.profile.gender = gender
            request.user.profile.save()

            #User Model
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.username = username
            request.user.email = email
            request.user.save()

            messages.success(request, "Profile updated successfully! Your changes have been saved.")
            return redirect('profile:update_profile')
        except Exception as error:
            messages.error(request, f"Failed to update the profile. {error}")
    return render(request, 'profile/update_profile.html', {
        'title': 'Update Profile',
    })

@login_required
def update_password(request):
    if request.method == 'POST':
        try:
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_new_password = request.POST['confirm_new_password']

            if request.user.check_password(old_password):
                if new_password == confirm_new_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, 'Password updated successfully!')
                    return redirect('main:signin')
                else:
                    messages.error(request, 'Failed to update password. New password does not match.')
                    return redirect('profile:update_password')
            else:
                messages.error(request, 'Failed to update password. Old password does not match.')
                return redirect('profile:update_password')
        except Exception as error:
            messages.error(request, f'Failes to update the password, {error}')
    return render(request, 'profile/update_password.html',{
        'title': 'Change Password',
    })