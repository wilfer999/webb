# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
# from json import dumps
# from django.contrib.auth.models import User
from koomper.common.models import Size


class UploadSerializers(serializers.Serializer):

    file = serializers.FileField(required=True)


class ChangeIdiomSerializers(serializers.Serializer):

    idiom = serializers.ChoiceField(
        choices=[
            ('en', 'English'),
            ('es', 'Espanol')]
    )


class SizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'
