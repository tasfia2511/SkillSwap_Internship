from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

from .forms import (
    ProfileForm,
    UserProfileForm,
    UserUpdateForm,
    CustomUserCreationForm,
)

from .models import UserProfile, SkillMatch


# ============================================================
# STATIC / FRONTEND PAGES
# ============================================================

def home(request):
    return render(
        request,
        'myapp/home.html'
    )


def about(request):
    return render(
        request,
        'myapp/about.html'
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            next_url = (
                request.POST.get('next')
                or request.GET.get('next')
            )

            if next_url:
                return redirect(next_url)

            return redirect('home')

    else:

        form = AuthenticationForm(request)

    return render(
        request,
        'myapp/login.html',
        {
            'form': form,
            'next': request.GET.get('next', '')
        }
    )


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = CustomUserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )

            return redirect('create_profile')

    else:

        form = CustomUserCreationForm()

    return render(
        request,
        'myapp/signup.html',
        {
            'form': form
        }
    )


# ============================================================
# PROFILE MANAGEMENT
# ============================================================

@login_required
def create_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            messages.success(
                request,
                'Your profile has been created successfully.'
            )

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'myapp/create_profile.html',
        {
            'form': form
        }
    )


@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                'Your profile has been updated successfully.'
            )

            return redirect('profile')

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = UserProfileForm(
            instance=profile
        )

    return render(
        request,
        'myapp/edit_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'myapp/profile.html',
        {
            'profile': profile
        }
    )


# ============================================================
# SERVICES
# ============================================================

def services(request):

    return render(
        request,
        'myapp/services.html'
    )


def service_detail(request, category):

    services_data = {

        'technology': {
            'title': 'Technology',
            'description': (
                'Learn and share practical technology skills '
                'with other members of the SkillSwap community.'
            ),
            'skills': [
                'Python',
                'Django',
                'Java',
                'C++',
                'JavaScript',
                'React',
                'Node.js',
                'Web Development',
                'Git & GitHub',
                'Database & SQL',
            ],
        },

        'creative-arts': {
            'title': 'Creative Arts',
            'description': (
                'Explore creative skills and learn from people '
                'who are passionate about art and design.'
            ),
            'skills': [
                'Drawing',
                'Digital Art',
                'Graphic Design',
                'Illustration',
                'Photography',
                'Video Editing',
                'UI/UX Design',
            ],
        },

        'music': {
            'title': 'Music',
            'description': (
                'Share your musical knowledge and learn from '
                'other musicians and music enthusiasts.'
            ),
            'skills': [
                'Guitar',
                'Piano',
                'Singing',
                'Music Theory',
                'Songwriting',
                'Music Production',
            ],
        },

        'languages': {
            'title': 'Languages',
            'description': (
                'Practice languages with other learners and '
                'experienced speakers.'
            ),
            'skills': [
                'English',
                'Spanish',
                'French',
                'German',
                'Arabic',
                'Japanese',
                'Public Speaking',
            ],
        },

        'professional-career': {
            'title': 'Professional / Career',
            'description': (
                'Build professional skills that can help you '
                'grow academically and professionally.'
            ),
            'skills': [
                'Public Speaking',
                'Communication',
                'Resume Writing',
                'Interview Preparation',
                'Leadership',
                'Marketing',
                'Networking',
            ],
        },
    }

    service = services_data.get(category)

    if service is None:
        return redirect('services')

    return render(
        request,
        'myapp/service_detail.html',
        {
            'service': service,
            'category': category,
        }
    )


# ============================================================
# FIND MATCHES
# ============================================================

@login_required
def find_matches(request):

    current_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if (
        not current_profile.skills_have.strip()
        or not current_profile.skills_want.strip()
    ):

        messages.info(
            request,
            'Please add the skills you have and the skills you want to learn first.'
        )

        return redirect('edit_profile')

    wanted_skills = [
        skill.strip().lower()
        for skill in current_profile.skills_want.split(',')
        if skill.strip()
    ]

    offered_skills = [
        skill.strip().lower()
        for skill in current_profile.skills_have.split(',')
        if skill.strip()
    ]

    other_profiles = UserProfile.objects.exclude(
        user=request.user
    )

    matches = []

    for other in other_profiles:

        other_have = [
            skill.strip().lower()
            for skill in other.skills_have.split(',')
            if skill.strip()
        ]

        other_want = [
            skill.strip().lower()
            for skill in other.skills_want.split(',')
            if skill.strip()
        ]

        can_teach_me = [
            skill
            for skill in wanted_skills
            if skill in other_have
        ]

        i_can_teach = [
            skill
            for skill in offered_skills
            if skill in other_want
        ]

        if can_teach_me and i_can_teach:

            matches.append({
                'profile': other,
                'can_teach_me': can_teach_me,
                'i_can_teach': i_can_teach,
            })

    return render(
        request,
        'myapp/find_matches.html',
        {
            'matches': matches
        }
    )


# ============================================================
# SEND MATCH REQUEST
# ============================================================

@login_required
def send_match_request(request, user_id):

    if request.method != 'POST':
        return redirect('find_matches')

    receiver_profile = get_object_or_404(
        UserProfile,
        user_id=user_id
    )

    if receiver_profile.user == request.user:

        messages.error(
            request,
            'You cannot send a match request to yourself.'
        )

        return redirect('find_matches')

    current_profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    wanted_skills = [
        skill.strip().lower()
        for skill in current_profile.skills_want.split(',')
        if skill.strip()
    ]

    receiver_skills = [
        skill.strip().lower()
        for skill in receiver_profile.skills_have.split(',')
        if skill.strip()
    ]

    matching_skills = [
        skill
        for skill in wanted_skills
        if skill in receiver_skills
    ]

    if not matching_skills:

        messages.error(
            request,
            'There is no matching skill for this request.'
        )

        return redirect('find_matches')

    skill = matching_skills[0]

    match, created = SkillMatch.objects.get_or_create(
        sender=request.user,
        receiver=receiver_profile.user,
        skill=skill
    )

    if created:

        messages.success(
            request,
            f'Match request sent to '
            f'{receiver_profile.user.username}.'
        )

    else:

        messages.info(
            request,
            'You already sent a request for this skill.'
        )

    return redirect('find_matches')


# ============================================================
# MY MATCHES
# ============================================================

@login_required
def match_list(request):

    received_requests = (
        SkillMatch.objects
        .filter(
            receiver=request.user,
            accepted=False
        )
        .select_related('sender')
    )

    sent_requests = (
        SkillMatch.objects
        .filter(
            sender=request.user,
            accepted=False
        )
        .select_related('receiver')
    )

    accepted_matches = (
        SkillMatch.objects
        .filter(
            Q(sender=request.user) |
            Q(receiver=request.user),
            accepted=True
        )
        .select_related(
            'sender',
            'receiver'
        )
    )

    return render(
        request,
        'myapp/match_list.html',
        {
            'received_requests': received_requests,
            'sent_requests': sent_requests,
            'accepted_matches': accepted_matches,
        }
    )


# ============================================================
# ACCEPT MATCH
# ============================================================

@login_required
def accept_match(request, match_id):

    if request.method != 'POST':
        return redirect('match_list')

    match = get_object_or_404(
        SkillMatch,
        id=match_id,
        receiver=request.user
    )

    match.accepted = True

    match.save()

    messages.success(
        request,
        f'You are now connected with '
        f'{match.sender.username}.'
    )

    return redirect('match_list')


# ============================================================
# REJECT MATCH
# ============================================================

@login_required
def reject_match(request, match_id):

    if request.method != 'POST':
        return redirect('match_list')

    match = get_object_or_404(
        SkillMatch,
        id=match_id,
        receiver=request.user
    )

    match.delete()

    messages.info(
        request,
        'Match request rejected.'
    )

    return redirect('match_list')


# ============================================================
# LEGACY MATCH VIEW
# ============================================================

def match_view(request):

    return redirect('match_list')


# ============================================================
# API-LIKE PROFILE CRUD
# ============================================================

@login_required
def create_profile_api(request):

    if request.method == 'POST':

        skills_have = request.POST.get(
            'skills_have',
            ''
        )

        skills_want = request.POST.get(
            'skills_want',
            ''
        )

        UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'skills_have': skills_have,
                'skills_want': skills_want,
            }
        )

        return JsonResponse({
            'message': 'Profile created successfully'
        })

    return JsonResponse(
        {
            'error': 'Invalid request'
        },
        status=400
    )


@login_required
def update_profile_api(request):

    if request.method == 'POST':

        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        profile.skills_have = request.POST.get(
            'skills_have',
            profile.skills_have
        )

        profile.skills_want = request.POST.get(
            'skills_want',
            profile.skills_want
        )

        profile.save()

        return JsonResponse({
            'message': 'Profile updated successfully'
        })

    return JsonResponse(
        {
            'error': 'Invalid request'
        },
        status=400
    )


@login_required
def delete_profile_api(request):

    if request.method == 'DELETE':

        try:

            profile = UserProfile.objects.get(
                user=request.user
            )

            profile.delete()

            return JsonResponse({
                'message': 'Profile deleted successfully'
            })

        except UserProfile.DoesNotExist:

            return JsonResponse(
                {
                    'error': 'Profile does not exist'
                },
                status=404
            )

    return JsonResponse(
        {
            'error': 'Invalid request'
        },
        status=400
    )