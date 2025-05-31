from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def main(request):
    
    return render(request,"main/main.html",{});