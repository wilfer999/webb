# Stdlib imports
from json import loads
# from requests import get
# Core Django imports
from django.utils import translation
# from django.contrib.auth import get_user_model
# from django.core.cache import cache
# Third-party app imports
# Imports from your apps
from koomper.common.models import Country
from koomper.common.utils import Base

# from json import loads


class Controller(Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.data = self.valid_data()
        self.error = {}
        self.result = []
        self.url_api = "http://"+self.request.META['HTTP_HOST']+"/api/v0/"

    def get_country(self):
        __country = Country.objects.prefetch_related(
            'country_state', 'country_state__state_city').all()

        __array = []
        for i in __country:
            __dict = {
                'id': i.id,
                'name': i.name,
                'code': i.code,
                'phone_code': i.phone_code,
                'tz': i.tz,
                'state': []
            }
            for s in i.country_state.all():
                __dict2 = {
                    'id': s.id,
                    'name': s.name,
                    'city': []
                }
                for c in s.state_city.all():
                    __dict3 = {
                        'id': c.id,
                        'name': c.name
                    }
                    __dict2['city'].append(__dict3)
                __dict['state'].append(__dict2)
            __array.append(__dict)
        self.result = __array

    def change_idiom(self):
        if not self._list_basic_info(self.data, ['idiom']):
            return

        user_language = self.data.get('idiom')
        translation.activate(user_language)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    def current_idiom(self):
        # import ipdb; ipdb.set_trace()
        try:
            self.result = self.request.session[translation.LANGUAGE_SESSION_KEY]
        except:
            user_language = "en"
            translation.activate(user_language)
            self.request.session[translation.LANGUAGE_SESSION_KEY] = user_language
            self.result = self.request.session[translation.LANGUAGE_SESSION_KEY]
