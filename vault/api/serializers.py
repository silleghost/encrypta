from rest_framework import serializers

from vault.models import Categories, Records


class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"