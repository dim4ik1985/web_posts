from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, User, Comment
from posts.permissions import IsAdminOrSelf, IsAdminOrAuthor
from posts.serializers import UserSerializer, PostSerializer, CommentSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':  # Регистрация доступна всем
            return [AllowAny()]
        if self.action in ['update', 'partial_update']:  # Обновление доступно только пользователю и админу
            return [IsAdminOrSelf()]
        elif self.action == 'destroy':   # Удаление доступно только админу
            return [IsAdminUser()]
        return [IsAuthenticated()]    # Чтение доступно только авторизованным пользователям или админу

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]

    # Автоматически назначаем автора при создании
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create': # CREATE: авторизованные пользователи.
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:  # UPDATE, DELETE: администратор/пользователь может редактировать/удалять только себя.
            return [IsAdminOrAuthor()]
        return [AllowAny()]  # READ: все пользователи.


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    # Автоматически назначаем автора при создании
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    def get_permissions(self):
        if self.action == 'create': # CREATE: авторизованные пользователи.
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:  # UPDATE, DELETE: администратор/пользователь может редактировать/удалять только себя.
            return [IsAdminOrAuthor()]
        return [AllowAny()]  # READ: все пользователи.


