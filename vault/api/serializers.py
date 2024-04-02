from rest_framework import serializers

from vault.models import Categories, Records


class RecordsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Records
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Categories
        fields = "__all__"