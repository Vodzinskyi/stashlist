from django.http import JsonResponse
from django.shortcuts import render

from .models import List
from django.contrib.auth.decorators import login_required

@login_required
def add_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            new_list = List.objects.create(name=name, owner=request.user)
            return JsonResponse({'status': 'ok'})
    return render(request, 'sidebar.html', {'error': 'Invalid data'})
