from rest_framework import serializers

from .models import Body, Car, Mark


def _car_photo(car):
    if not car:
        return None
    if car.photo:
        return car.photo.url
    return car.photo_url or None


class BodyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ('id', 'name', 'slug')


class MarkBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'name', 'slug')


class BodySerializer(serializers.ModelSerializer):
    car_count = serializers.IntegerField(read_only=True)
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Body
        fields = ('id', 'name', 'slug', 'car_count', 'cover_photo')

    def get_cover_photo(self, obj):
        car = obj.cars.exclude(photo_url='').first() or obj.cars.first()
        return _car_photo(car)


class MarkSerializer(serializers.ModelSerializer):
    car_count = serializers.IntegerField(read_only=True)
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Mark
        fields = ('id', 'name', 'slug', 'car_count', 'cover_photo')

    def get_cover_photo(self, obj):
        car = obj.cars.exclude(photo_url='').first() or obj.cars.first()
        return _car_photo(car)


class CarListSerializer(serializers.ModelSerializer):
    mark = MarkBriefSerializer(read_only=True)
    body = BodyBriefSerializer(read_only=True)
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
