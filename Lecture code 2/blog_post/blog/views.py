from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.filtersets import BlogPostFilter
from blog.models import BlogPost, Author
from blog.pagination import BlogPostPagination, BlogPostOffsetPagination, BlogPostCursorPagination
from blog.serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer, AuthorSerializer
)

class BlogPostListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostListSerializer
    pagination_class = BlogPostPagination
    # filterset_fields = ['category', 'title']
    filterset_class = BlogPostFilter


class BlogPostDetailViewSet(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostDetailSerializer


class BlogPostUpdateViewSet(mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostCreateUpdateSerializer


class BlogPostCreateViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostCreateUpdateSerializer


class  BlogPostDeleteViewSet(mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostListSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    # pagination_class = BlogPostOffsetPagination
    # pagination_class = BlogPostCursorPagination
    filterset_class = BlogPostFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        elif self.action == 'create' or self.action == 'update':
            return BlogPostCreateUpdateSerializer
        else:
            return BlogPostListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "total_products": queryset.count(),
                "paginated_results": serializer.data
            })
        # If pagination is not used
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "total_products": queryset.count(),
            "paginated_results": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            kwargs['fields'] = ('first_name', 'last_name')
        elif self.action == 'update':
            kwargs['fields'] = ('first_name', 'last_name', 'email')
        return super().get_serializer(*args, **kwargs)
