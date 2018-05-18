from django.shortcuts import render
from .models import Board

def boards_home(request):
    boards = Board.objects.all()
    return render(request, 'boards/home.html', {'boards': boards})
