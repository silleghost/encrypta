import jwt
from encrypta.settings import SECRET_KEY
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from vault.api.serializers import CategoriesSerializer, RecordsSerializer
from vault.models import Categories, Records


class RecordsViewSet(ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer

    def get_queryset(self):
        try:
            token = self.request.headers["Authorization"].split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            user_queryset = Records.objects.filter(user_id=user_id).order_by('app_name')
            return user_queryset
        except:
            # return Response({"error": "Недействительный токен"})
            return Records.objects.none()

    @action(methods=["get"], detail=False)
    def categories(self, request):
        try:
            token = self.request.headers["Authorization"].split()[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
        except jwt.exceptions.DecodeError:
            return Response({"error": "Недействительный токен"})
        cats = Categories.objects.filter(user_id=user_id)
        return Response({"cats": [c.name for c in cats]})


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        try:
            token = self.request.headers["Authorization"].split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            return Categories.objects.filter(user_id=user_id)
        except:
            return Response({"error": "Недействительный токен"})