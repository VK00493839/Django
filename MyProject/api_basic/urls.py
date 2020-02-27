from django.urls import path, include
from .views import ArticleAPIView, ArticleDetails, GenericAPIView, ArticleViewsets, ArticleGenericViewset, ArticleModelViewSet
from rest_framework.routers import DefaultRouter

# getting error because of Class Based APIView
# TypeError at /viewset/article/ 'Object of type ListSerializer is not JSON serializable'
# router = DefaultRouter()
# router.register('article', ArticleViewsets, basename='article')

# router = DefaultRouter()
# router.register('article', ArticleGenericViewset, basename='article')

router = DefaultRouter()
router.register('article', ArticleModelViewSet, basename='article')


urlpatterns = [
    # Class Based API Views
    path('article/', ArticleAPIView.as_view()),
    path('detail/<int:id>/', ArticleDetails.as_view()),

    # Generic Views & Mixins
    path('generic/article/<int:id>/', GenericAPIView.as_view()),

    # Viewsets and Routers
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
]