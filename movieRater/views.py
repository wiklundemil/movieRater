from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def apiV1(request):
    api_urls = {
        'Create':'/user-create/',
        'Read':'/user-read/',
        'Update':'/user-update/',
        'Delete':'/user-delete/',
    }
    return Response(api_urls)