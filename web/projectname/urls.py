"""
URL configuration for projectname project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from home.views import *
from auth.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("mentor/", mentor, name="mentor"),
    path("student/", student, name="student"),
    path("translate/", translate_content, name="translate_content"),
    path("generate-ai-answer/", generate_ai_answer_view, name="generate_ai_answer"),
    path("delete-question/<int:question_id>/", delete_question, name="delete_question"),
]
