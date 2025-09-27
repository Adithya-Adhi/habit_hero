
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Habit, CheckIn, Category
from .serializers import HabitSerializer, CheckInSerializer, CategorySerializer

@api_view(["GET", "POST"])
def habit_list(request):
    if request.method == "GET":
        habits = Habit.objects.all().order_by("-id")
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def habit_detail(request, pk):
    try:
        habit = Habit.objects.get(pk=pk)
    except Habit.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HabitSerializer(habit)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = HabitSerializer(habit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(["GET", "POST"])
def checkin_list(request):
    if request.method == "GET":
        habit_id = request.GET.get("habit")
        if habit_id:
            checkins = CheckIn.objects.filter(habit_id=habit_id).order_by("-date")
        else:
            checkins = CheckIn.objects.all().order_by("-date")
        serializer = CheckInSerializer(checkins, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CheckInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def generate_report(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="habit_progress_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(72, y, "Habit Hero - Progress Report")
    y -= 30
    p.setFont("Helvetica", 10)

    for habit in Habit.objects.all():
        if y < 120:
            p.showPage()
            y = 750
        p.drawString(72, y, f"Habit: {habit.name}  |  Frequency: {habit.frequency}  |  Start: {habit.start_date}")
        y -= 18
        checkins = habit.checkins.all().order_by("-date")
        if checkins.exists():
            for c in checkins:
                if y < 100:
                    p.showPage()
                    y = 750
                p.drawString(90, y, f"- {c.date}: {c.note or ''}")
                y -= 14
        else:
            p.drawString(90, y, "- No check-ins yet")
            y -= 14
        y -= 6

    p.showPage()
    p.save()
    return response
