from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    head = request.headers
    return HttpResponse(str(head))
