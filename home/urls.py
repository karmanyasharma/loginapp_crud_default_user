from django.contrib import admin
from django.urls import path,include

from home import views

urlpatterns = [
    path('', views.index,name="home"),
    path('login/', views.loginUser,name="login"),  # Include URLs from the home app
    path('signup/', views.signupUser,name="signup"),  
    path('user/', views.addUsers,name="addUsers"),  
    path('list/', views.listUsers,name="listUsers"),  
    path('view/<int:id>', views.viewDetailofuser,name="detail"),  
    path('edit/<int:id>', views.editUser,name="editUser"),  
    path('delete/<int:id>', views.deleteUser,name="deleteUser"), 
    path('logout/', views.logoutUser,name="logout"),  
    path('contact/',views.about,name="about")
]