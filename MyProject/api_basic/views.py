from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.utils import encoders
from rest_framework import generics,mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Create your views here.
# -->Viewsets and Routers
# using ViewSet we need to use all methods list(), retrieve(), create(), update()
# getting error because of Class Based APIView
# TypeError at /viewset/article/ 'Object of type ListSerializer is not JSON serializable'
class ArticleViewsets(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)

# --> GenericViewSet using with mixins
class ArticleGenericViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.CreateModelMixin,mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # to update the objects we need to UpdateModelMixin with RetrieveModelMixin

# -->ModelViewSet
# with this we dont even use GenericView and Mixins we can get all methods even without implementing
class ArticleModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


# -->Generic Views & Mixins
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                     mixins.CreateModelMixin,mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,mixins.RetrieveModelMixin):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'
    # -->Authentication
    # authentication_classes = [SessionAuthentication, BaseAuthentication] # uses Username and password
    # atleast one permission class should be there
    authentication_classes = [TokenAuthentication] # uses token to authorize 'user'; Creates another table
    permission_classes = [IsAuthenticated]

    # It just lists out the objects using ListModelMixin
    def get(self, request, id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    # post the objects using CreateModelMixin then it will show POST form in UI Page
    def post(self, request):
        return self.create(request)

    # update the objects using UpdateModelMixin it shows another form below POST
    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


# -->Class Based API Views # getting error here
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialzer = ArticleSerializer(data=request.data)

        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.data, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.get_object(id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)