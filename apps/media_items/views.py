from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.media_items.models import MediaItem


@method_decorator([csrf_exempt], name='dispatch')
class MediaItemView(View):
    #def patch(self, request, pk):

    def delete(self, request, list_id, pk):
        try:
            item = MediaItem.objects.get(id=pk, owner=request.user)
            item.delete()
            return HttpResponse("", content_type="text/html")
        except MediaItem.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
