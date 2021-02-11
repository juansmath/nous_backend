from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

class BaseViewSet(viewsets.ViewSet):
    model = None
    serializer_class = None
    queryset = None

    def get_queryset(self):
        return self.queryset

    def list(self, request):
        data = self.get_queryset()
        data = serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)