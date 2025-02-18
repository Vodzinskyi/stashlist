from urllib.parse import parse_qs

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import List

@method_decorator([csrf_exempt], name='dispatch')
class ListView(View):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request, pk=None):
        if pk:
            try:
                item = List.objects.get(id=pk, owner=request.user)
                return JsonResponse({"id": item.id, "name": item.name})
            except List.DoesNotExist:
                return JsonResponse({"error": "Not found"}, status=404)
        else:
            lists = List.objects.filter(owner=request.user).values("id", "name")
            return JsonResponse(list(lists), safe=False)


    def post(self, request):
        name = request.POST.get('name')
        if name:
            new_list = List.objects.create(name=name, owner=request.user)
            return JsonResponse({"id": new_list.id, "name": new_list.name})
        return JsonResponse({"error": "Invalid request"}, status=400)


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
            item.delete()
            return JsonResponse({"success": True})
        except List.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

