from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter



from blog_post.models import BlogPost, Reaction, Comment
from blog_post.serializers import (UserSerializer,
                                   BlogPostSerializer,
                                   ReactionSerializer,
                                   CommentSerializer,
                                   PostStatesSerializer)
from blog_post.permissions import IsAuthorOrReadOnly, IsReaderOrReadOnly
from blog_post.tasks import send_registration_email
from blog_post.paginations import PostPagination



class UserRegistrationAPIView(APIView):
    """
    Create User and sends email to user after successfully registeration.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_registration_email.delay(user.email)  #TODO configure in signals 
            return Response({
                    "id": user.id,
                    "username": user.username,
                    "role": user.bloguser.role
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    """Create Post and reaction to the posts(Like comments and views)."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = BlogPost.objects.select_related("author").order_by("title")
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = [
        "author_id", "created_at", 
    ]
    ordering_fields = ['views']
    serializer_class = BlogPostSerializer
    pagination_class = PostPagination
    page_size = 10


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Detail of Post with each call post view counts get incremented."""

        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def react(self, request, pk=None):
        """React to a Post."""

        post = self.get_object()
        reaction_type = request.data.get('reaction')

        if reaction_type not in [Reaction.ReactionChoices.LIKE, Reaction.ReactionChoices.DISLIKE]:
            return Response({"error": "Invalid reaction."}, status=status.HTTP_400_BAD_REQUEST)

        reaction, _ = Reaction.objects.update_or_create(
            user=request.user.bloguser, post=post,
            defaults={'reaction': reaction_type}
        )
        return Response(ReactionSerializer(reaction).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsReaderOrReadOnly])
    def comment(self, request, pk=None):
        """Adding a comment to the Post."""

        post = self.get_object()
        content = request.data.get('content', "")
        if content:
            comment = Comment.objects.create(user=request.user.bloguser, post=post, content=content)
            return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
        return Response({"Error": "Please provide the content in the comment"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], serializer_class=PostStatesSerializer)
    def stats(self, request, pk=None):
        """Stats of a particular Post."""

        post = self.get_object()
        post_serializer = self.get_serializer_class()
        return Response(post_serializer(post).data, status=status.HTTP_200_OK)