from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateThought, GoalForm, EditProfilePicForm
from django.db import IntegrityError
from django.http import  HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .filters import ThoughtFilter
import json

from .models import User, Thought, Goal, Rewards

# Create your views here.

MILESTONES = {
    1: "First goal is completed! Congratulations!",
    5: "You completed 5 goals! Keep up the good work!",
    10: "You completed 10 goals!",
    20: "You completed 20 goals!",
    40: "You completed 40 goals!",
    60: "You completed 60 goals!",
    100: "You completed 100 goals! Amazing!"
}

def index(request):
    form = CreateThought()    
    return render(request, "yinyang/index.html",{
        "nform": form,
        "pform": form
    })

@login_required
def dashboard_view(request, id):
    user = User.objects.get(pk=id)
    all_logs = Thought.objects.filter(author=user).order_by("-timestamp")[0:8]
    form = GoalForm()
    goals = Goal.objects.filter(user=request.user).all()
    tag_choices = list(Thought._meta.get_field("tag").choices)

    badges = Rewards.objects.filter(receiver=user, reward_type="BADGE")
    return render(request, "yinyang/dashboard.html", {
        "user": user,
        "all_logs": all_logs,
        "form": form,
        "goals": goals,
        "badges": badges,
        "tag_choices": tag_choices
    })

@login_required
def profile_view(request, id):
    user = User.objects.get(pk=id)
    earned_badges = Rewards.objects.filter(receiver=user, reward_type="BADGE").values_list("description", flat=True)    

    # List of all available badges
    all_badges = [
        {"description": "First goal is completed! Congratulations!", "name": "First Steps"},
        {"description": "You completed 5 goals! Keep up the good work!", "name": "High Five"},
        {"description": "You completed 10 goals!", "name": "Pathfinder"},
        {"description": "You completed 20 goals!", "name": "Trailblazer"},
        {"description": "You completed 40 goals!", "name": "Goal Master"},
        {"description": "You completed 60 goals!", "name": "Ambition Architect"},
        {"description": "You completed 100 goals! Amazing!", "name": "Century Champion"},
    ]

    return render(request, "yinyang/profile.html", {
        "user": user,
        "earned_badges": earned_badges,
        "all_badges": all_badges
    })

def logs_view(request, id):
    user = User.objects.get(pk=id)
    all_logs = Thought.objects.filter(author=user).order_by("-timestamp")    

    sort = request.GET.get('sort', 'newest')
    if sort == 'newest':
        all_logs = all_logs.order_by("-timestamp")
    else:
        all_logs = all_logs.order_by("timestamp")

    f = ThoughtFilter(request.GET, queryset=all_logs)
    tag_choices = list(Thought._meta.get_field("tag").choices)

    paginator = Paginator(f.qs, 6)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)    

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        logs_data = []
        for obj in page_obj:
            logs_data.append({
                "id": obj.id,
                "entry": obj.entry,
                "timestamp": obj.timestamp.strftime('%d %b %Y'),
                "tag": obj.tag,
            })
        return JsonResponse({
            "logs": logs_data,
            "has_next": page_obj.has_next(),
            "log_count": paginator.count,
        })

    return render(request, "yinyang/logs.html", {
        "user": user,
        "all_logs": all_logs,
        "filter": f,
        "page_obj": page_obj,
        "tag_choices": tag_choices
    })

def load_more(request, id):
    loaded_item = int(request.GET.get("loaded_item", 0))    
    limit = 2
    sort_value = request.GET.get('sort', 'newest')
    # Determine sorting direction
    if sort_value == 'newest':
        ordering = '-timestamp'
    else:
        ordering = 'timestamp' 
    filter_params = request.GET.dict()   
    log_obj = list(Thought.objects.filter(author_id=id, **filter_params).order_by(ordering).values()[loaded_item:loaded_item+limit])   
    return JsonResponse({"status": "success", "logs": log_obj})

class LogsListView(ListView):
    paginate_by = 10
    model = Thought

def new_negative_thought(request):
    if request.method =="POST":
        nform = CreateThought(request.POST)
        if nform.is_valid():
            new_entry = nform.save(commit=False)
            new_entry.author = request.user
            new_entry.thought_type = "NEGATIVE"
            new_entry.save()
            return redirect("index")
        else:
            nform = CreateThought()
            return render(request, "yinyang/index.html", {
            "nform": nform
            })
    return render(request, "yinyang/index.html")

def new_positive_thought(request):
    if request.method =="POST":
        pform = CreateThought(request.POST)
        if pform.is_valid():
            new_entry = pform.save(commit=False)
            new_entry.author = request.user
            new_entry.thought_type = "POSITIVE"
            new_entry.save() 
            return redirect("index")
        else:
            pform = CreateThought()
            return render(request, "yinyang/index.html", {
            "pform": pform
            })
    return render(request, "yinyang/index.html")

def set_goal(request):
    if request.method == "POST":
        if Goal.objects.filter(user=request.user, is_completed=False).count() >= 5:
            return JsonResponse({"success": False, "message": "You have reached maximun number of goals"}, status=400)
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return JsonResponse({"success": True, "goal": {
                "id": goal.id,
                "description": goal.description,
                "category": goal.category}, 
                "message": "New goal is set" 
                })
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@login_required
def complete_goal(request, goal_id):
    if request.method == "POST":
        user = request.user
        goal = Goal.objects.get(pk=goal_id,user=user)
        goal.is_completed = not goal.is_completed
        goal.save()

        new_badge = None
        completed_goals_count = Goal.objects.filter(user=user, is_completed=True).count()    
        if completed_goals_count in MILESTONES:
            new_badge = MILESTONES[completed_goals_count]
            award_badge(user, completed_goals_count)

        return JsonResponse({
            "success": True,
            "goal": goal.id,
            "is_completed": goal.is_completed,
            "new_badge": new_badge
            })
    return JsonResponse({"error": "Invalid request method."}, status=400)

def chart_data_thoughts(request, id):
    user = User.objects.get(pk=id)
    data = {
        "negative": list(
            Thought.objects.filter(author=user, thought_type="NEGATIVE").values("tag").annotate(count=Count("tag"))
         ),
        "positive": list(
            Thought.objects.filter(author=user, thought_type="POSITIVE").values("tag").annotate(count=Count("tag"))
        ),
    }
    return JsonResponse(data)

def chart_data_goals(request, id):
    user = User.objects.get(pk=id)
    data = {
        "goals": list(
            Goal.objects.filter(user=user).values("category").annotate(count=Count("category"))
         )
    }
    return JsonResponse(data)

def award_badge(user, completed_goals_count):
    user.badges += 1
    user.save()

    # Create a reward entry for the badge
    reward_description = MILESTONES[completed_goals_count]
    Rewards.objects.create(
        receiver=user,
        reward_type="BADGE",
        description=reward_description
    )

def get_rewards(request, id):
    user = User.objects.get(pk=id)
    rewards = Rewards.objects.filter(receiver=user, reward_type="BADGE")
    rewards_data = []  
    for reward in rewards:
        rewards_data.append({
            "id": reward.id,
            "description": reward.description
        })
    return JsonResponse({"rewards": rewards_data})

@csrf_exempt
def edit_log(request, log_id):
    if request.method == "PUT":
        log = Thought.objects.get(pk=log_id)
        data = json.loads(request.body)
        log_content = data.get("entry", " ").strip()
        log_tag = data.get("tag")

        if not log_content:
            return JsonResponse({"error": "Entry cannot be empty."}, status=400)        
        
        log.entry = log_content
        log.tag = log_tag
        log.edited = True
        log.save()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400) 

def delete_log(request, log_id):
    if request.method == "DELETE":
        try:
            log = Thought.objects.get(pk=log_id)
            log.delete()
            return JsonResponse({"status": "success","message": "Log deleted successfully"}, status=200)
        except Thought.DoesNotExist:
            return JsonResponse({"error": "Log not found."}, status=404)
    else:
        return render(request, "yinyang/dashboard.html")
        
def delete_goal(request, goal_id):
    if request.method == "DELETE":
        try:
            goal = Goal.objects.get(pk=goal_id)
            goal.delete()
            return JsonResponse({"status": "success","message": "Goal deleted successfully"}, status=200)
        except Goal.DoesNotExist:
            return JsonResponse({"error": "Goal not found."}, status=404)
    else:
        return render(request, "yinyang/dashboard.html")
    
@login_required
def edit_profile_pic(request):    
    if request.method == "POST":
        image_form = EditProfilePicForm(request.POST, request.FILES)
        if image_form.is_valid():
            user = request.user
            user.image = image_form.cleaned_data["image"]
            user.save() 
            return redirect("profile", id=request.user.id)
        else:
            image_form = EditProfilePicForm(request.user)
        return render(request, "yinyang/profile.html", {
            "image_form": image_form
        })
    
@login_required
def completed_goals_list(request, id):
    user = User.objects.get(pk=id)
    completed_goals = Goal.objects.filter(user=user, is_completed=True)
    return render(request, "yinyang/completed_goals.html", {
            "completed_goals": completed_goals
        })

    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "yinyang/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "yinyang/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "yinyang/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "yinyang/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "yinyang/register.html")    
