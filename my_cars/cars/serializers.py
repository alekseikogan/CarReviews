from rest_framework import serializers

from .models import Body, Car, Mark


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ('id', 'name', 'slug')


class MarkSerializer(serializers.ModelSerializer):
    car_count = serializers.SerializerMethodField()

    class Meta:
        model = Mark
        fields = ('id', 'name', 'slug', 'car_count')

    def get_car_count(self, obj):
        return obj.cars.count()


class CarListSerializer(serializers.ModelSerializer):
    mark = MarkSerializer(read_only=True)
    body = BodySerializer(read_only=True)
    photo_display = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            'id', 'slug', 'mark', 'model', 'complect', 'body',
            'description', 'year', 'photo_display', 'time_create',
        )

    def get_photo_display(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return obj.photo_url


class CarDetailSerializer(CarListSerializer):
    class Meta(CarListSerializer.Meta):
        fields = CarListSerializer.Meta.fields
