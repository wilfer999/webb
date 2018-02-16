from rest_framework import serializers
from django.contrib.auth import get_user_model
from koomper.rotator.models import (Banner, Library)
from django.utils.translation import ugettext_lazy as _
# from json import dumps
User = get_user_model()


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ('name', 'width', 'height', 'id')


class LibrarySerializer(serializers.Serializer):

        file = serializers.FileField(required=True)
        name = serializers.CharField()
        # url_file = serializers.CharField()


class RotatorSerializer(serializers.Serializer):

        name = serializers.CharField()
        banner_id = serializers.SlugRelatedField(
                queryset=Banner.objects.filter(status=True), slug_field='id')
        library_id = serializers.SlugRelatedField(
                queryset=Library.objects.filter(status=True), slug_field='id')
        # library_id = serializers.CharField()
        types = serializers.ChoiceField(choices=[('1', 'Image'),
                                                 ('2', 'HTML')])
        html = serializers.CharField()
        url_site = serializers.CharField()
        # date_time_start = serializers.DateTimeField()
        # date_time_end = serializers.DateTimeField()


class RotatorUpdateSerializer(serializers.Serializer):

    name = serializers.CharField()
    url_site = serializers.CharField()
    date_time_start = serializers.DateTimeField()
    date_time_end = serializers.DateTimeField()


class PauseRotatorSerializer(serializers.Serializer):

    banner_id = serializers.SlugRelatedField(
                queryset=Banner.objects.filter(status=True), slug_field='id')
    pause = serializers.BooleanField()


class PauseRotator1Serializer(serializers.Serializer):

    pause = serializers.BooleanField()


class ActionBannerSerializer(serializers.Serializer):
    __action = (
        (1, _("randow")),
        (2, _("porcent")),
        (3, _("CTR"))
    )
    action_rotator = serializers.ChoiceField(choices=__action)
    rotator = serializers.CharField(help_text='[{"id": 1, "porcent": 100}]')


class ActionBanner1Serializer(serializers.Serializer):

    pause = serializers.BooleanField()


class SaveAllRotatorSerializer(serializers.Serializer):
    __action = (
        (1, _("randow")),
        (2, _("porcent")),
        (3, _("CTR"))
    )
    banner_id = serializers.SlugRelatedField(
                queryset=Banner.objects.filter(status=True), slug_field='id')
    rotator = serializers.CharField(
        help_text='[{"name": "manuel", "library_id": "1","html": "html","types": "1", "url_site": "http://www.google.co.ve"}, {"name": "manuel", "html": "html","html_file": "html_file", "types": "2", "url_site": "http://www.google.co.ve"}, {"id": "id", "name": "manuel", "library_id": "1","html": "html","types": "2", "url_site": "http://www.google.co.ve"}]')
