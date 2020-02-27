from rest_framework import  serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['id','title','author']
        fields = '__all__'

    # def create(self,validated_data):
    #     return Article.objects.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.save()
    #     return instance