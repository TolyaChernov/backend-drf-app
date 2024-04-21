import requests
from bs4 import BeautifulSoup
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser

from .models import Collection, Link
from .permissions import IsOwnerOrReadOnly
from .serializers import CollectionSerializer, LinkSerializer


class CollectionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    # permission_classes = [IsAuthenticated]


class CollectionRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsOwnerOrReadOnly]


class LinkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        url = request.data.get("url")
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        # Получение данных из Open Graph мета-тегов
        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        # Если мета-теги Open Graph не найдены, получаем данные из тегов title
        # и meta description
        if not og_title:
            title = soup.title.string.strip() if soup.title else None
        else:
            title = og_title.get("content")

        if not og_description:
            description = None
        else:
            description = og_description.get("content")

        if not og_image:
            image = None
        else:
            image = og_image.get("content")
        # Создание объекта Link

        user = CustomUser.objects.get(email=request.user)

        # Проверяем, есть ли указанные коллекции и принадлежат ли они
        # пользователю
        collections_ids = request.data.get("collections", [])
        print("collections_ids: ", collections_ids)
        collections_of_user = Collection.objects.filter(user=user)
        print("collections_of_user: ", collections_of_user)
        if collections_ids and not all(
            [collection in collections_of_user for collection in collections_ids]
        ):
            return Response(
                {
                    "detail": "Одна или несколько указанных коллекций не принадлежат вам."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        link_data = {
            "url": url,
            "title": title,
            "description": description,
            "image": image,
            "collections": request.data.get("collections"),
            "user": user.id,
        }

        all_links_of_user = Link.objects.filter(user=user)
        for link in all_links_of_user:
            print(link.url)
        if url in [link.url for link in all_links_of_user]:
            return Response(
                {"detail": "Такая ссылка уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("link_data: ", link_data)

        serializer = self.get_serializer(data=link_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LinkRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsOwnerOrReadOnly]
