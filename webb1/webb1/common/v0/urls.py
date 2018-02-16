from rest_framework import routers
from common.v0.views import (
    UploadView, CountryView, ChangeIdiomView,
    SizeViewsets
    )

router = routers.DefaultRouter()

router.register(r'upload', UploadView, base_name='upload')
router.register(r'countries', CountryView, base_name='countries')
router.register(r'language', ChangeIdiomView, base_name='language')
router.register(r'size', SizeViewsets, base_name='size')
# router.register(r'upload', UploadView, base_name='upload_file')
