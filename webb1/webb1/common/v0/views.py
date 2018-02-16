# Third-party app imports
from rest_framework import viewsets
# Imports from your apps
from common.utils import default_responses, UploadFile
from .api import Controller
from rest_framework import permissions
from .serializers import (
    UploadSerializers, ChangeIdiomSerializers, SizeSerializers)
from koomper.common.models import Size
# from login.models import Profile

# from common.pagination import LinkHeaderPagination
# from rest_framework import generics
# from json import loads


class UploadView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UploadSerializers
    """
    HOOLA
    """
    def create(self, request, *args, **kwargs):

        serializer = UploadFile(request)
        serializer.upload()

        if serializer.error:
            print(serializer.error)
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class CountryView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    """
    Get Country
    """

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_country()

        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class ChangeIdiomView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ChangeIdiomSerializers

    """
    Change Language
    """

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.current_idiom()

        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)

    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.change_idiom()

        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class SizeViewsets(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SizeSerializers

    def get_queryset(self):
        return Size.objects.filter(status=True)
