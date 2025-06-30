from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Photo, Tag, UserProfile
from .forms import PhotoForm, ProfileForm, CustomUserCreationForm

def home(request):
    tag = request.GET.get('tag')
    photos = Photo.objects.filter(tags__name=tag) if tag else Photo.objects.all()
    tags = Tag.objects.all()
    return render(request, 'home.html', {'photos': photos, 'tags': tags})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_detail.html', {'photo': photo})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('photo_gallery:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

