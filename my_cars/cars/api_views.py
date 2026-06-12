from django.db.models import Count, Q
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Body, Car, Mark
from .serializers import BodySerializer, CarDetailSerializer, CarListSerializer, MarkSerializer


class MarkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mark.objects.annotate(car_count=Count('cars')).order_by('name')
    serializer_class = MarkSerializer
    lookup_field = 'slug'
    pagination_class = None


class BodyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Body.objects.annotate(car_count=Count('cars')).order_by('name')
    serializer_class = BodySerializer
    lookup_field = 'slug'
    pagination_class = None


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.select_related('mark', 'body').all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CarDetailSerializer
        return CarListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        mark = self.request.query_params.get('mark')
        body = self.request.query_params.get('body')
        search = self.request.query_params.get('search')
        if mark:
            qs = qs.filter(mark__slug=mark)
        if body:
            qs = qs.filter(body__slug=body)
        if search:
            qs = qs.filter(
                Q(model__icontains=search) | Q(mark__name__icontains=search),
            )
        return qs

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response({
            'total_cars': Car.objects.count(),
            'total_marks': Mark.objects.count(),
            'total_bodies': Body.objects.count(),
        })
