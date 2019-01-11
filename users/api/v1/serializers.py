from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name', 'email', 'avatar')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        self.user = authenticate(username=data.get("username"), password=data.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError('User disabled')
            return data
        else:
            raise serializers.ValidationError('Invalid credentials')
