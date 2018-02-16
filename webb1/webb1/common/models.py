from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=3)
    phone_code = models.CharField(max_length=200)
    tz = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    class Meta:
        app_label = 'common'
        db_table = 'country'

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='country_state')
    status = models.BooleanField(default=True)

    class Meta:
        app_label = 'common'
        db_table = 'states'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name="state_city")
    status = models.BooleanField(default=True)

    class Meta:
        app_label = 'common'
        db_table = 'city'

    def __str__(self):
        return self.name


class TimeZone(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'common'
        db_table = 'time_zone'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        app_label = 'common'
        db_table = 'size'

    def __str__(self):
        return self.name
