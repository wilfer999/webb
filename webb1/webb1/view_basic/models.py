from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import date


class Restaurant(models.Model):
    name = models.TextField()
    street = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    city = models.TextField(default="")
    zipCode = models.TextField(blank=True, null=True)
    stateOrProvince = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    telephone = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    # user = models.ForeignKey(User, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,
    #                          related_name='banner_u', null=True)
    date = models.DateField(default=date.today)

    def __unicode__(self):
        return u"%s" % self.name


class Dish(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField('Euro amount', max_digits=8, decimal_places=2, blank=True, null=True)
    # user = models.ForeignKey(User, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    date = models.DateField(default=date.today)
    image = models.ImageField(upload_to="myrestaurants", blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, null=True, related_name='dishes')

    def __unicode__(self):
        return u"%s" % self.name


class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    # user = models.ForeignKey(User, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True

class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant)


# class Library(models.Model):
#     name = models.CharField(max_length=100, null=False)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE,
#                              related_name='library_user', null=True)
#     file = models.CharField(max_length=100, null=False)
#     content_type = models.CharField(max_length=100, null=False)
#     size = models.CharField(max_length=100, null=False)
#     name_file = models.CharField(max_length=100, null=False)
#     status = models.BooleanField(default=True)
#     create_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         app_label = 'rotator'
#         db_table = 'library'

#     def __str__(self):
#         return self.name
