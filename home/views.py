from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages 


@login_required(login_url='/home/login/')
def index(request):
    return render(request, 'index.html')



def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')   
        else:
            
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect(reverse("login")) 


def about(request):
    return render(request, 'about.html')

def signupUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_pass=request.POST.get('confirmpassword')
        if password!=confirm_pass:
            messagee="Password and Confirm Password do not match"
            return render(request, 'register.html', {'message': messagee})
        if User.objects.filter(username=username).exists():
            messagee="Username already exists"
            return render(request, 'register.html', {'message': messagee})
        user=User.objects.create_user(username=username,password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    return render(request, 'register.html')

def isadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(isadmin,login_url='/home/login/')
def addUsers(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_pass=request.POST.get('confirmpassword')
        if password!=confirm_pass:
            messagee="Password and Confirm Password do not match"
            return render(request, 'addUsers.html', {'message': messagee})
        if User.objects.filter(username=username).exists():
            messagee="Username already exists"
            return render(request, 'addUsers.html', {'message': messagee})
        user=User.objects.create_user(username=username,password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('/home/')
    return render(request, 'addUsers.html')

@user_passes_test(isadmin,login_url='/home/login/')
def listUsers(request):
    user= User.objects.all()
    context = {
        'users': user
    }
    return render(request, 'listUser.html',context)

@user_passes_test(isadmin, login_url='/home/login')
def viewDetailofuser(request,id):
    user=User.objects.get(pk=id)
    return render(request, 'viewDetail.html', {'user':user})

@user_passes_test(isadmin, login_url='/home/login')
def editUser(request, id):
    user = get_object_or_404(User, pk=id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('detail', id=user.id)
    
    
    return render(request, 'editUser.html', {'user': user})

@user_passes_test(isadmin,login_url='/home/login')
def deleteUser(request,id):
    user=get_object_or_404(User,pk=id)
    user.delete()
    return redirect('listUsers')


