from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True,style={"input_type":"password"})

    class Meta:
        model=User
        fields=['username','email','password','password2']
        extra_kwargs={
            "username":{"write_only":True}
        }

    def save(self):
        password=self.validated_data['password']

        if password!=self.validated_data['password2']:
            raise serializers.ValidationError({"error":"The password confirmation Failed!"})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error":"User with that email already exists!"})

        new_user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
