from common.utils import Base
from koomper.rotator.models import (Banner, Library, Rotator, Analitycs)
# from common.utils import default_responses, UploadFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from json import loads
from datetime import (datetime, timedelta)
# import json()
from django.template.loader import render_to_string
from django_bulk_update.helper import bulk_update
from koomper.rotator.models import Device, OS, Browser, Analitycs
from koomper.common.models import Country, City, TimeZone
from django.utils.translation import ugettext_lazy as _
from json import loads
# import re
# from django.conf import settings
# # from datetime import datetime
# from requests import get
# from django.utils.dateparse import parse_datetime
# from common.utils import ThreadDef
from ipware.ip import get_ip
import imgkit


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        if not self.request.FILES:
            try:
                self.data = self.valid_data()
            except:
                self.data = {}
        self.url_api = "http://"+self.request.META['HTTP_HOST']+"/api/v0/"
        self.pytracking_config = {
            "webhook_url": "http://"+request.META['HTTP_HOST'],
            "base_open_tracking_url": self.url_api + "banner/open/",
            "base_click_tracking_url": self.url_api + "banner/click/",
            "default_metadata": {"analytics_key": "123456"}
        }

    def valid_create_banner(self, kwargs):
        __valid = [
            'name', 'width', 'height'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        if not self.list_only_string(self.data, ["name"]):
            return

        if not self._list_int_info(self.data, ['width', 'height']):
            return

        return True

    def list_banner(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __search = self.request.GET.get('search')
        __filters.update({"status": True})
        # __filters.update({"user_id": self.request.user.id})
        self.list_banners(__filters, __paginator, __ordening, __search)

    def list_banner_u(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __filters.update({"user_id": self.request.user.id})
        __search = self.request.GET.get('search')
        __filters.update({"status": True})
        # __filters.update({"user_id": self.request.user.id})
        self.list_banners(__filters, __paginator, __ordening, __search)

    def list_banners(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        __p = Banner.objects.filter(
            **filters).prefetch_related('banner_rotator').order_by(*ordening)

        for i in __p:
            __dict = {
                "id": i.id,
                "name": i.name,
                "width": i.width,
                "height": i.height,
                "status": i.status,
                'action_rotator': i.action_rotator,
                'action_rotator_name': i.get_action_rotator_display(),
                'rotator': [],
                "create_at": i.create_at,
            }
            for e in i.banner_rotator.all():
                __dict2 = {
                    "id": e.id,
                    "name": e.name,
                    "html_file": "http://"+self.request.META['HTTP_HOST']+"/media/"+str(e.html_file),
                    "library": {
                        "name": e.library.name,
                        "url": "http://"+self.request.META['HTTP_HOST']+"/media/"+ e.library.file,
                        "file": e.library.file,
                        "status": e.library.status,
                        "create_at": str(e.library.create_at)
                    } if e.library_id else {},
                    "html": e.html,
                    "types": e.types,
                    "date_time_start": e.date_time_start,
                    "date_time_end": e.date_time_end,
                    "status": e.status,
                    "url_site": e.url_site,
                    "token": e.token,
                    "imp": e.imp,
                    "click": e.click,
                    "crt": e.crt,
                    "percent": e.percent,
                    "pause": e.pause,
                    "create_at": e.create_at,
                }
                __dict['rotator'].append(__dict2)
            __array.append(__dict)

        if not filters.get('pk'):
            # import ipdb; ipdb.set_trace()
            self.paginator(__array, paginator)
            print(paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]

    def create_banner(self):

        self.data = self.request.data
        print(self.data)
        if not self.valid_create_banner(self.data):
            return

        self.export_attr(Banner, self.data)
        self.values['user_id'] = self.request.user.id
        create = Banner.objects.create(**self.values)
        self.result = create.id

    def update_banner(self, id_banner):
        print(self.request.data)
        self.data = self.request.data
        if not self.valid_create_banner(self.data):
            return
        update = Banner.objects.filter(id=id_banner, status=True)
        if not update:
            self._error_info(_("ID Banner"), _("not exit"))
            return
        update[0].name = self.data.get('name')
        update[0].width = self.data.get('width')
        update[0].height = self.data.get('height')
        update[0].save()
        x = self.list_banner(id_banner)
        self.result = x

    def delete_banner(self, id_banner):
        # print(self.request.data)
        self.data = self.request.data
        Banner.objects.filter(id=id_banner, status=True).update(status=False)

    def valid_create_library(self, kwargs):
        __valid = [
            'name', 'file'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        return True

    def create_library(self):
        self.data = self.request.data
        print(self.data)
        if not self.valid_create_library(self.data):
            return
        __files = self.request.FILES['file']
        # import ipdb; ipdb.set_trace()
        fl = __files
        __name = self.remove_space_string(__files.name)
        __files = default_storage.save(
            'tmp_media/' + __name,
            ContentFile(__files.read()))
        self.export_attr(Library, self.data)
        self.values["user_id"] = self.request.user.id
        self.values['file'] = __files
        self.values['content_type'] = fl.content_type
        self.values['size'] = fl.size
        self.values['name_file'] = fl.name
        create = Library.objects.create(**self.values)
        self.get_library(create.id)

    def get_library(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        if pk:
            __filters.update({'pk': pk})
        __filters.update({'status': True})
        __array = []
        for i in Library.objects.filter(**__filters):
            __dict = {
                    'id': i.id,
                    'name': i.name,
                    'url_update': self.url_api+"library/"+str(i.id),
                    'status': i.status,
                    'content_type': i.content_type,
                    'size': i.size,
                    'name_file': i.name_file,
                    'file': "http://"+self.request.META['HTTP_HOST']+"/media/"+i.file,
                    'user': {
                        "user_id": i.user.id,
                        "user_name": i.user.name,
                        "user_country": i.user.country,
                        "user_company": i.user.company,
                        "user_position": i.user.position,
                        "user_status": i.user.status,
                        "create_user": i.user.create_at
                        },
                    'create_at': i.create_at
            }
            __array.append(__dict)

        if not __filters.get('pk'):
            self.paginator(__array, __paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array
        # return __array
            self.result = __array[0]
        return __array

    def get_library_u(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __filters.update({"user_id": self.request.user.id})
        __paginator = loads(self.request.GET.get('paginator', "{}"))

        if pk:
            __filters.update({'pk': pk})
        __array = []
        __filters.update({'status': True})
        for i in Library.objects.filter(**__filters):
            __dict = {
                    'id': i.id,
                    'name': i.name,
                    'url_update': self.url_api+"library/"+str(i.id),
                    'status': i.status,
                    'content_type': i.content_type,
                    'size': i.size,
                    'name_file': i.name_file,
                    'file': "http://"+self.request.META['HTTP_HOST']+"/media/"+i.file,
                    'user': {
                        "user_id": i.user.id,
                        "user_name": i.user.name,
                        "user_country": i.user.country,
                        "user_company": i.user.company,
                        "user_position": i.user.position,
                        "user_status": i.user.status,
                        "create_user": i.user.create_at
                        },
                    'create_at': i.create_at
            }

            __array.append(__dict)

        if not __filters.get('pk'):
            self.paginator(__array, __paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array
        # return __array
            self.result = __array[0]
        return __array

    def delete_library(self, library_id):
        self.data = self.request.data
        if not Library.objects.filter(id=library_id):
            self._error_info(_("ID Library"), _("not exit"))
            return
        delete = Library.objects.get(id=library_id)
        delete.status = False
        delete.save()
        x = self.get_library(delete.id)
        self.result = x

    def valid_create_rotator(self, kwargs):
        __valid = [
            'name', 'banner_id', 'types', 'url_site'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        # import ipdb; ipdb.set_trace()
        if kwargs.get('types') == 1:
            __valid = [
                'library_id'
            ]
            if not self._list_basic_info(kwargs, __valid):
                return
        else:
            __valid = [
                'html'
            ]
            if not self._list_basic_info(kwargs, __valid):
                return

        return True

    def create_rotator(self):
        # print("aqui esta:" + str(self.request.data))

        if not self.valid_create_rotator(self.data):
            return
        date1 = datetime.now()
        date2 = timedelta(days=90)
        dates = date1 + date2
        print(dates)
        self.export_attr(Rotator, self.data)
        self.values["date_time_start"] = date1
        self.values["date_time_end"] = dates
        create = Rotator.objects.create(**self.values)
        if self.data.get('html'):
            tmp = "tmp_media/" + str(create.id) + self.generator() + '.jpg'
            html = "koomper/media/"+tmp
            imgkit.from_string(
                self.data.get('html'),
                html)
            create.html_file = tmp
            create.save()
        # import ipdb; ipdb.set_trace()
        self.result = {
            "id": create.id,
            "name": create.name,
            "url_update": self.url_api+"rotator/"+str(create.id),
            "html": create.html,
            "types": create.types,
            "url_site": create.url_site,
            "click": create.click,
            "crt": create.crt,
            "percent": create.percent,
            "status": create.status,
            "create_at": create.create_at,
            "date_time_start": create.date_time_start,
            "date_time_end": create.date_time_end,
            # "library_id": create.library_id,
            "library": {
                "id": create.library_id,
                "name": create.library.name,
                "url": "http://"+self.request.META['HTTP_HOST']+"/media/"+create.library.file,
                "status": create.library.status,
                "create_at": create.library.create_at,
            } if create.library_id else {},

        }

    def get_rotator(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        if pk:
            __filters.update({'pk': pk})
        rotator = Rotator.objects.filter(**__filters)
        __array = []
        for x in rotator:
            __dict2 = {
                "rotador_id": x.id,
                "html_file": "http://"+self.request.META['HTTP_HOST']+"/media/"+str(x.html_file),
                "name": x.name,
                "url_update": self.url_api+"rotator/"+str(x.id),
                "html": x.html,
                "types": x.types,
                "url_site": x.url_site,
                "click": x.click,
                "crt": x.crt,
                "percent": x.percent,
                "status": x.status,
                "create_at": x.create_at,
                "date_time_start": x.date_time_start,
                "date_time_end": x.date_time_end,
                "library": {
                    # "library_id": x.library.id,
                    "id": x.library.id,
                    "name": x.library.name,
                    "url": "http://"+self.request.META['HTTP_HOST']+"/media/"+x.library.file,
                    "status": x.library.status,
                    "create_at": x.library.create_at,
                    "user": {
                        "user_id": x.library.user.id,
                        "user_name": x.library.user.name,
                        "user_country": x.library.user.country,
                        "user_company": x.library.user.company,
                        "user_position": x.library.user.position,
                        "user_status": x.library.user.status,
                        "create_user": x.library.user.create_at
                    },
                } if x.library else {},
            }
            __array.append(__dict2)

        if not __filters.get('pk'):
            self.paginator(__array, __paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array
        return __array

    def update_rotator(self, id_rotator):
        print(self.request.data)
        self.data = self.request.data
        __valid = [
            'name', 'url_site'
        ]
        if not self._list_basic_info(self.data, __valid):
            return

        update = Rotator.objects.filter(id=id_rotator, status=True)
        if not update:
            self._error_info(_("ID Rotator"), _("not exit"))
            return
        x1 = update[0]
        # if self.data.get('html'):
        #     tmp = "tmp_media/" + str(create.id) + self.generator() + '.jpg'
        #     html = "koomper/media/"+tmp
        #     imgkit.from_string(
        #         self.data.get('html'),
        #         html)
        #     create.html_file = tmp
        #     create.save()
        x1.html = self.data.get('html')
        x1.name = self.data.get('name')
        x1.url_site = self.data.get('url_site')
        x1.save()
        x = self.get_rotator(id_rotator)
        self.result = x

    def delete_rotator(self, rotator_id):
        self.data = self.request.data
        if not Rotator.objects.filter(id=rotator_id):
            self._error_info(_("ID Rotator"), _("is not exit"))
            return
        delete = Rotator.objects.get(id=rotator_id)
        delete.status = False
        delete.save()
        x = self.get_rotator(delete.id)
        self.result = x

    def get_tracking(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        if pk:
            __filters.update({'pk': pk})
        track = Analitycs.objects.filter(**__filters)
        __array = []
        for i in track:
            print(i)
            __dict = {
                "id_track": i.id,
                "option": i.option,
                "os": i.os.name,
                "browser": i.browser.name,
                "device": i.device.name,
                "country": {
                    "id": i.country.id,
                    "name": i.country.name,
                    "phone_code": i.country.phone_code,
                    "city": {
                        "id": i.city.id,
                        "name": i.city.name,
                        "state": {
                            "id": i.city.state.id,
                            "name": i.city.state.name,
                        },
                    },
                },
                "time_zone": i.timezone.name,
                "create_rotator": i.create_at
            }
            # __dict["rotator"].append(__dict2)
            __array.append(__dict)

        if not __filters.get('pk'):
            self.paginator(__array, __paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array
        return __array

    def browser(self):
        # import ipdb; ipdb.set_trace()
        __browser, value = Browser.objects.get_or_create(
            name=self.request.user_agent.browser.family,
            version=self.request.user_agent.browser.version_string
            )
        return __browser

    def os(self):
        __os, value = OS.objects.get_or_create(
            name=self.request.user_agent.os.family,
            version=self.request.user_agent.os.version_string
            )
        return __os

    def device(self):
        # import ipdb; ipdb.set_trace()
        __device, value = Device.objects.get_or_create(
            name=self.request.user_agent.device.family,
            branch=self.request.user_agent.device.brand,
            model=self.request.user_agent.device.model
            )
        return __device

    def track_rotator(self, option=1, pk=None):
        # import ipdb; ipdb.set_trace()
        if pk:
            self.data = {}
            self.data['rotator'] = pk

        if not self.data.get('rotator'):
            self._error_info(_("Rotator"), _("is required"))
            return
        # import ipdb; ipdb.set_trace()
        ip = get_ip(self.request)
        self.geoip2(ip)
        country = Country.objects.filter(
            name__icontains=self.geo_info.get('country'))
        __city = City.objects.filter(state__country__name__icontains=country[0].id if country else '', name__icontains=self.geo_info.get('city') if self.geo_info.get('city') else '')
        timezone, value = TimeZone.objects.get_or_create(name=self.geo_info.get('time_zone')) if self.geo_info.get('time_zone') else None
        # import ipdb; ipdb.set_trace()
        dict2 = {
            "option": option,
            "rotator_id": self.data.get('rotator'),
            "browser_id": self.browser().id,
            "os_id": self.os().id,
            "device_id": self.device().id,
            "country_id": country[0].id if country else None,
            "city_id": __city[0].id if __city else None,
            "timezone_id": timezone.id,
            "is_mobile": self.request.user_agent.is_mobile,
            "is_tablet": self.request.user_agent.is_tablet,
            "is_touch_capable": self.request.user_agent.is_touch_capable,
            "is_pc": self.request.user_agent.is_pc,
            "is_bot": self.request.user_agent.is_bot,
        }

        # import ipdb; ipdb.set_trace()
        __analitycs = Analitycs.objects.create(**dict2)
        self.result = __analitycs.rotator.url_site

    def valid_pause_rotator(self, kwargs):
        # import ipdb; ipdb.set_trace()
        if not self._list_int_info(kwargs, ['banner_id']):
            return

        try:
            self.__banner = Banner.objects.get(
                id=kwargs.get('banner_id'), status=True)
        except:
            self._error_info(_("ID Banner"), _("not exit"))
            return

        return True

    def pause_rotator(self):

        if not self.valid_pause_rotator(self.data):
            return

        self.__banner.banner_rotator.all().update(
            pause= True if self.data.get('pause') else False)

        self.result = [i for i in self.__banner.banner_rotator.all().values()]

    def list_rotator(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __search = self.request.GET.get('search')
        __filters.update({"status": True})
        # __filters.update({"user_id": self.request.user.id})
        self.list_rotators(__filters, __paginator, __ordening, __search)

    def list_rotators(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        __p = Rotator.objects.filter(
            **filters).select_related('library').order_by(*ordening)

        for i in __p:

            __dict2 = {
                "id": i.id,
                "name": i.name,
                "html_file": "http://"+self.request.META['HTTP_HOST']+"/media/"+str(i.html_file),
                "library": {
                    "name": i.library.name,
                    "url": "http://"+self.request.META['HTTP_HOST']+"/media/"+ i.library.file,
                    "file": i.library.file,
                    "status": i.library.status,
                    "create_at": str(i.library.create_at)
                },
                "html": i.html,
                "types": i.types,
                "date_time_start": i.date_time_start,
                "date_time_end": i.date_time_end,
                "status": i.status,
                "url_site": i.url_site,
                "token": i.token,
                "imp": i.imp,
                "click": i.click,
                "crt": i.crt,
                "percent": i.percent,
                "pause": i.pause,
                "create_at": i.create_at,
            }
            __array.append(__dict2)

        if not filters.get('pk'):
            # import ipdb; ipdb.set_trace()
            self.paginator(__array, paginator)
            print(paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]

    def pause_rotator_id(self, pk):

        __rotator = Rotator.objects.filter(id=pk)
        if not __rotator:
            self._error_info(_("ID Rotator"), _("not exit"))
            return
        __rotator.update(pause=True if self.data.get('pause') else False)
        self.list_rotator(pk)

    def valid_change_action(self, kwargs):
        print("hello")
        # import ipdb; ipdb.set_trace()
        if not self._list_int_info(kwargs, ['action_rotator']):
            return

        if int(self.data.get('action_rotator')) == 2:
            if not self._list_basic_info(kwargs, ['rotator']):
                return
            try:
                kwargs['rotator'] = loads(kwargs.get('rotator'))
            except:
                self._error_info(_("Rotator"), _('it is not a Dict'))
                return
            __porcent = 0
            __array = []
            for i in kwargs.get('rotator'):
                if not self._list_basic_info(i, ['id', 'porcent']):
                    return
                __porcent += int(i.get('porcent'))
                if not i.get('id') in __array:
                    __array.append(i.get('id'))
            # import ipdb; ipdb.set_trace()
            if not __porcent == 100:
                self._error_info(_("Rotator"), _("must be equal 100"))
                return
            for i in self.__banner.banner_rotator.filter(status=True):
                if i.id not in __array:
                    self._error_info(_("Rotator") +str(i.id), _("must be in cycle"))
                    return

        return True

    def change_action(self, pk):
        try:
            self.__banner = Banner.objects.get(id=pk)
        except:
            self._error_info(_("ID Banner"), _("not exit"))
            return
        # import ipdb; ipdb.set_trace()
        if not self.valid_change_action(self.data):
            return
        # __banner.action_rotator = self.
        print("sd")
        self.__banner.action_rotator = self.data.get('action_rotator')
        self.__banner.save()
        if int(self.data.get('action_rotator')) == 2:
            for i in self.__banner.banner_rotator.filter(status=True):
                for e in self.data.get('rotator'):
                    if i.id == int(e.get('id')):
                        i.percent = e.get('porcent')
                        i.save()
        self.list_banner(pk)

    def save_all_rotator(self):
        # import ipdb; ipdb.set_trace()
        date1 = datetime.now()
        date2 = timedelta(days=90)
        dates = date1 + date2
        # print(self.data['rotator'])
        __array = []
        for i in loads(self.data['rotator']):
            # print(i['html'])
            if i.get('html'):
                print("FE")
                tmp = "tmp_media/" + str(self.request.user.id) + self.generator() + '.jpg'
                html = "koomper/media/"+tmp
                imgkit.from_string(
                    i['html'],
                    html)
                i.update({"html_file": tmp})
            self.export_attr(Rotator, i)
            self.values['banner_id'] = self.data.get('banner_id')
            self.values['date_time_start'] = date1
            self.values['date_time_end'] = dates
            __array.append(Rotator(**self.values))

        Rotator.objects.bulk_create(__array)

        self.result = Rotator.objects.filter(
            status=True, banner_id=self.data.get('banner_id')).values()
