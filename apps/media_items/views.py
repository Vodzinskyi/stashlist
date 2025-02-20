import json
from urllib.parse import parse_qs

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.media_items.models import MediaItem


@method_decorator([login_required, csrf_exempt], name='dispatch')
class MediaItemView(View):

    def patch(self, request, list_id, pk):
        media_item = get_object_or_404(MediaItem, id=pk)
        body = parse_qs(request.body.decode('utf-8'))
        title = body.get('title', [None])[0]
        description = body.get('description', [None])[0]
        if title and description:
            media_item.title = title
            media_item.description = description
            media_item.save()
            return HttpResponse(status=204)


    def delete(self, request, list_id, pk):
        try:
            item = MediaItem.objects.get(id=pk, owner=request.user)
            item.delete()
            return HttpResponse("", content_type="text/html")
        except MediaItem.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
