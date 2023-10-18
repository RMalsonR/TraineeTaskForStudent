from rest_framework import serializers

from trainee_task.core.models import User, Product, Lesson, LessonsView


class UserInProduct(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProductSerializer(serializers.ModelSerializer):
    owner = UserInProduct(many=False)

    class Meta:
        model = Product
        fields = ('id', 'title', 'owner')


class LessonsViewSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = LessonsView
        fields = ('duration', 'status', 'updated_at')


class LessonsListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    views = LessonsViewSerializer(many=False)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_link', 'duration', 'products', 'views')


class LessonsRetrieveSerializer(serializers.ModelSerializer):
    views = LessonsViewSerializer(many=False)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_link', 'duration', 'views')




