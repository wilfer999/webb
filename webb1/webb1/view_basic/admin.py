# from django.contrib import admin
# import models

# Register your models here.

from django.contrib import admin
from . import models
# import models

admin.site.register(models.Restaurant)
admin.site.register(models.Dish)
admin.site.register(models.RestaurantReview)
