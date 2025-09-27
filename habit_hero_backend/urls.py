
from django.contrib import admin
from django.urls import path
from habits import views

urlpatterns = [
    path("admin/", admin.site.urls),


    path("api/habits/", views.habit_list, name="habit-list"),
    path("api/habits/<int:pk>/", views.habit_detail, name="habit-detail"),


    path("api/checkins/", views.checkin_list, name="checkin-list"),

    path("api/categories/", views.category_list, name="category-list"),

    path("api/report/", views.generate_report, name="generate-report"),
]
