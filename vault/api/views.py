from multiprocessing import AuthenticationError
import jwt
from encrypta.settings import SECRET_KEY
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from vault.api.serializers import CategoriesSerializer, RecordsSerializer
from vault.models import Categories, Records


class RecordsViewSet(ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            token = self.request.headers["Authorization"].split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            return Records.objects.filter(user_id=user_id)
        except:
            raise AuthenticationError('Invalid token')
        


    @action(methods=['get'], detail=False)
    def categories(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            cats = Categories.objects.filter(user_id=user_id)
            return Response({'cats': [c.name for c in cats]})
        return Response({'error': 'user_id is required'})
    

class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    permission_classes = (IsAuthenticated,)