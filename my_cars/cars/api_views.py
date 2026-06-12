from django.db.models import Count, Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Body, Car, Comment, Mark
from .serializers import (
    BodySerializer,
    CarDetailSerializer,
    CarListSerializer,
    CommentSerializer,
    MarkSerializer,
)


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

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, slug=None):
        car = self.get_object()
        if request.method == 'GET':
            qs = car.comments.select_related('user').all()
            serializer = CommentSerializer(qs, many=True, context={'request': request})
            return Response(serializer.data)
        if not request.user.is_authenticated:
            return Response({'detail': 'Требуется авторизация.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, car=car)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDestroyView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
