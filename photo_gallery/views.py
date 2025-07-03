from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Photo, Tag, UserProfile
from .forms import PhotoForm, ProfileForm, CustomUserCreationForm
from django.db.models import Count
from .forms import EmailLoginForm



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

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            form.save_m2m()
            return redirect('photo_gallery:home')
    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})
@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo_gallery:photo_detail', pk=pk)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_gallery:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('photo_gallery:profile')
    template_name = 'change_password.html'

def most_liked_photos(request):
    photos = Photo.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    return render(request, 'most_liked.html', {'photos': photos})

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo_gallery:photo_detail', pk=pk)
def email_login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('photo_gallery:home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = EmailLoginForm()
    return render(request, 'login.html', {'form': form})


