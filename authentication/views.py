from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Issue, CustomUser
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def my_login(request):

    if request.method == "POST":
        # Get the form data
        username = request.POST["username"]
        password = request.POST["password"]
        user = CustomUser.objects.filter(username=username, password=password).first()
        users = CustomUser.objects.all()
        if user not in users:
            return render(request, "authentication/login.html", {"error": "Invalid user name or password."})
        
        is_valid = True if user is not None else False
                
             
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged in successfully.")

            return render(request, "authentication/index.html", {"name": username, "is_valid": is_valid})
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("home")
        
    return render(request, "authentication/login.html")

def register(request):
    
    if request.method == "POST":
        # Get the form data
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register", {"error": "Passwords do not match."})
        
        
        myUser = CustomUser.objects.create(username=username,
                                        email=email,
                                        password=password,
                                        confirm_password=confirm_password,
                                        first_name=first_name,
                                        last_name=last_name)
        
        myUser.save()
                
        return redirect("my_login")
    
    return render(request, "authentication/register.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")

@login_required(login_url="my_login")
def table(request):
    result = []
    users = request.user
    
    all_user_in_same_team = CustomUser.objects.filter(team = users.team)
    
    for user in all_user_in_same_team:
        result.extend(user.issues.all())
    
    return render(request, "table/table.html", {"result": result})

@login_required(login_url="my_login")
def add_issue(request):
    
    user = request.user
    users = CustomUser.objects.all()
    print(users)
    if request.method == "POST":
        # Get the form data
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        title = request.POST["title"]
        description = request.POST["description"]        
        asigned_user = request.POST["dropdownName"]
        issue = Issue()
        
        issue = Issue.objects.create(title=title, description=description, status="To Do", logged_time=0, date=current_time, asigned= asigned_user)
        issue.save()
        user.issues.add(issue)
        user.save()
        messages.success(request, "Record added successfully.")
        
        return redirect("table")
    
    return render(request, "table/add.html", {'users': users})

@csrf_exempt
def update_issue_status(request):
    if request.method == "POST":
        issue_id = request.POST.get("id")
        new_status = request.POST.get("status")
        
        try:
            issue = Issue.objects.get(id=issue_id)
            issue.status = new_status
            issue.save()
            return JsonResponse({"success": True})
        except Issue.DoesNotExist:
            return JsonResponse({"success": False, "error": "Issue not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url="my_login")
def update_issue(request, id):
    issue_queryset = Issue.objects.filter(id = id)
    users = CustomUser.objects.all()
    if request.method == "POST":
        action = request.POST.get('action') 
        issue = issue_queryset[0]
        if action == "save":
            new_title = request.POST.get('title')
            new_description = request.POST.get('description')
            new_logged_time = request.POST.get('logged_time')
            asigned_user_id = request.POST.get("dropdownName")
            asigned_user = CustomUser.objects.filter(id = asigned_user_id).first()
            print(asigned_user)
            
            issue.title = new_title
            issue.description = new_description
            issue.logged_time = new_logged_time
            issue.asigned = asigned_user
            issue.save()
            print("Issue updated")
            return redirect("table")
        
        if action == "delete_issue":
            issue.delete()
            print("Issue sucessfully deleted")
            return redirect("table")
    
    return render(request, "table/update.html", {"current_issue": issue_queryset[0], 'users': users})
