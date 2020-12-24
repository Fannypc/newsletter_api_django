from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tag
from .serializers import TagSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def newsletters(self, req, pk=None):
        tag = self.get_object()
        if req.method == 'GET':
            serializer = TagSerializer(tag.newsletters, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

