from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def getRoutes(request):
    routes = [
    ]

    return Response(routes)

def VaultListView(ListAPIView):
    """
    Возвращает все записи текущего пользователя.
    """
    pass

def RecordCreateView(CreateAPIView):
    """
    Сохраняет запись в базе данных.
    """
    pass

def RecordRetrieveView(RetrieveAPIView):
    """
    Получает данные выбранной записи по id.
    """
    pass

def RecordDestroyView(DestroyAPIView):
    """
    Удаляет запись по id.
    """
    pass
