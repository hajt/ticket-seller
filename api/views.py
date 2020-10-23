from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets

from api.models import (
    Event,
    TicketInfo,
    Ticket,
    Reservation,
)
from api.serializers import (
    EventSerializer,
    TicketInfoSerializer,
    TicketSerializer,
    ReservationSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()



# class EventList(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer


# class TicketKindList(generics.ListCreateAPIView):
#     queryset = TicketInfo.objects.all()
#     serializer_class = TicketInfoSerializer


# @csrf_exempt
# def events_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = EventSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def event_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         event = Event.objects.get(pk=pk)
#     except Event.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = EventSerializer(event)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = EventSerializer(event, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         event.delete()
#         return HttpResponse(status=204)
