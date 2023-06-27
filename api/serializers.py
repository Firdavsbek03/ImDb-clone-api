from rest_framework import serializers
from watchlist_app.models import Movie,StreamPlatform,Review


class ReviewSerializer(serializers.ModelSerializer):
    writer=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Review
        exclude=('movie',)
        # fields="__all__"


class MovieSerializer(serializers.ModelSerializer):
    # reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')

    class Meta:
        model=Movie
        fields="__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    movies=MovieSerializer(many=True,read_only=True)

    class Meta:
        model=StreamPlatform
        fields="__all__"

# def name_length(value):
#     if len(value)<3:
#         raise serializers.ValidationError("The movie name is too short")
# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name= serializers.CharField(max_length=200,validators=[name_length])
#     description=serializers.CharField()
#     active=serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("The movie name and description shouldn't be the same")
#         return data
#
#     # def validate_name(self,value):
#     #     if len(value)<3:
#     #         raise serializers.ValidationError("The Movie Name is too Short")
#     #     return value
