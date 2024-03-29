from rest_framework import serializers

from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, max_length=256, style={"input_type" : "password"}, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



