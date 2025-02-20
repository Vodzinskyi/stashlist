from urllib.parse import parse_qs

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import List
from ..media_items.models import MediaItem


@method_decorator([csrf_exempt], name='dispatch')
class ListView(View):

    def post(self, request):
        name = request.POST.get('name')
        if name:
            new_list = List.objects.create(name=name, owner=request.user)
            return JsonResponse({"id": new_list.id, "name": new_list.name})
        return JsonResponse({"error": "Invalid request"}, status=400)

    def get(self, request):
        lists = List.objects.filter(owner=request.user).values("id", "name")
        return JsonResponse(list(lists), safe=False)


@method_decorator([csrf_exempt], name='dispatch')
class ListDetailView(View):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request, pk):
        try:
            media_list = List.objects.get(id=pk, owner=request.user)
            media_items = media_list.items.all()
            if request.headers.get('HX-Request') == 'true':
                return render(request, 'list.html', {'list': media_list, 'items': media_items})
            return render(request, 'index.html', {'list': media_list, 'items': media_items})
        except List.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

    def post(self, request, pk):
        title = request.POST.get('title')
        description = request.POST.get('description')
        media_item = MediaItem.objects.create(title=title, description=description, owner=request.user)
        media_list = List.objects.get(pk=pk)
        media_list.items.add(media_item)
        return render(request, 'media_item.html', {'item': media_item})

    def patch(self, request, pk):
        try:
            item = List.objects.get(id=pk, owner=request.user)
            body = parse_qs(request.body.decode('utf-8'))
            name = body.get('name', [None])[0]
            if name:
                item.name = name
                item.save()
                return HttpResponse(status=204)
            return JsonResponse({"error": "Name is required"}, status=400)

        except List.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

    def delete(self, request, pk):
        try:
            item = List.objects.get(id=pk, owner=request.user)
            is_current = request.headers.get('HX-Current-URL', '').endswith(f'/lists/{pk}/')
            item.delete()
            if is_current:
                return HttpResponse("", headers={
                    "HX-Reswap": "innerHTML",
                    "HX-Retarget": "#list-container",
                    "HX-Redirect": reverse('index')
                })
            return JsonResponse({"success": True})
        except List.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)


