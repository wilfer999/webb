from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
# Imports from your apps
from common.utils import default_responses
from .api import Controller
from .serializers import (BannerSerializer, LibrarySerializer,
                          RotatorSerializer, RotatorUpdateSerializer,
                          PauseRotatorSerializer, PauseRotator1Serializer,
                          ActionBannerSerializer, SaveAllRotatorSerializer)


class ControlBanner(viewsets.ViewSet):

    serializer_class = BannerSerializer
    """
    SECTION OF CREATE BANNER, FIRST STEP FOR CREATE ROTATOR
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.create_banner()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        if request.user.level == 1:
            serializer.list_banner()
        else:
            serializer.list_banner_u()

        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = BannerSerializer
        serializer = Controller(request)
        serializer.list_banner(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.update_banner(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)

    def delete(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_banner(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class ControlLibrary(viewsets.ViewSet):

    serializer_class = LibrarySerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    def create(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        serializer = Controller(request)
        serializer.create_library()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        if request.user.level == 1:
            serializer.get_library()
        else:
            serializer.get_library_u()

        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = LibrarySerializer

        return default_responses(200, pk)

    def destroy(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_library(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class ControlRotator(viewsets.ViewSet):

    serializer_class = RotatorSerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.create_rotator()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = RotatorUpdateSerializer

        return default_responses(200, pk)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.update_rotator(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)

    def destroy(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_rotator(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class TrackingRotator(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    # serializer_class = RotatorSerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.track_rotator()
        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_tracking()
        # serializer.track_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = RotatorUpdateSerializer

        return default_responses(200, pk)

    # def update(self, request, pk, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.update_rotator(pk)
    #     if serializer.error:
    #         return default_responses(404, serializer.error)

    #     return default_responses(200, serializer.result)

    # def destroy(self, request, pk, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.delete_rotator(pk)
    #     if serializer.error:
    #         return default_responses(404, serializer.error)

    #     return default_responses(200, serializer.result)


class LibraryHtml(viewsets.ViewSet):

    serializer_class = LibrarySerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    def create(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        serializer = Controller(request)
        serializer.create_library()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    # def list(self, request, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.get_library()
    #     if serializer.error:
    #         print(serializer.error)
    #         return default_responses(400, serializer.error)

    #     return default_responses(200, serializer.result)

    # def retrieve(self, request, pk, *args, **kwargs):
    #     self.serializer_class = LibrarySerializer

    #     return default_responses(200, pk)

    # def destroy(self, request, pk, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.delete_library(pk)
    #     if serializer.error:
    #         print(serializer.error)
    #         return default_responses(404, serializer.error)

    #     return default_responses(200, serializer.result)


class PauseRotator(viewsets.ViewSet):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = PauseRotatorSerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.pause_rotator()
        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.list_banner()
        # serializer.track_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = PauseRotator1Serializer
        serializer = Controller(request)
        serializer.list_rotator(pk)
        # serializer.track_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.pause_rotator_id(pk)
        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)


class ActionBanner(viewsets.ViewSet):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = ActionBannerSerializer
    """
    SECTION OF LIBRARY, NOT EXIST UPDATE IN FRONT END PRODUCTION
    """
    # def create(self, request, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.pause_rotator()
    #     if serializer.error:
    #         return default_responses(404, serializer.error)
    #     print(serializer.result)
    #     return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.list_banner()
        # serializer.track_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.list_banner(pk)
        # serializer.track_rotator()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.change_action(pk)
        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)


class AllRotator(viewsets.ViewSet):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = SaveAllRotatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.save_all_rotator()
        if serializer.error:
            return default_responses(404, serializer.error)
        # print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        return default_responses(200, {})
