from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo, Tag, UserProfile

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