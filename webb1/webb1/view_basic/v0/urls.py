from django.conf.urls import url, include
from rest_framework import routers
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView


# from models import Restaurant, Dish
# from forms import RestaurantForm, DishForm
# from views import RestaurantCreate, DishCreate, RestaurantDetail

router = routers.DefaultRouter()

# urlpatterns = [


#     url(r'\^\$',
#         ListView.as_view(
#         	queryset=Restaurant.objects.filter(date__lte=timezone.now()).order_by('date')[:5],
#         	context_object_name='latest_restaurant_list',
#         	template_name='myrestaurants/restaurant_list.html'),
#         name='restaurant_list'),

# # Restaurant details, ex.: /myrestaurants/restaurants/1/
#     url(r'\^restaurants/(?P<pk>\d+)/\$',
#         RestaurantDetail.as_view(),
#         name='restaurant_detail'),

# # Restaurant dish details, ex: /myrestaurants/restaurants/1/dishes/1/
#     url(r'\^restaurants/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/\$',
#         DetailView.as_view(
#         	model=Dish,
#         	template_name='myrestaurants/dish_detail.html'),
#         name='dish_detail'),

# # Create a restaurant, /myrestaurants/restaurants/create/
#     url(r'\^restaurants/create/\$',
#         RestaurantCreate.as_view(),
#         name='restaurant_create'),

# # Edit restaurant details, ex.: /myrestaurants/restaurants/1/edit/
#     url(r'\^restaurants/(?P<pk>\d+)/edit/\$',
#         UpdateView.as_view(
#         	model = Restaurant,
#         	template_name = 'myrestaurants/form.html',
#         	form_class = RestaurantForm),
#         name='restaurant_edit'),

# # Create a restaurant dish, ex.: /myrestaurants/restaurants/1/dishes/create/
#     url(r'\^restaurants/(?P<pk>\\d+)/dishes/create/\$',
#     	DishCreate.as_view(),
#         name='dish_create'),

# # Edit restaurant dish details, ex.: /myrestaurants/restaurants/1/dishes/1/edit/
#     url(r'\^restaurants/(?P<pkr>\\d+)/dishes/(?P<pk>\\d+)/edit/\$',
#     	UpdateView.as_view(
#     		model = Dish,
#     		template_name = 'myrestaurants/form.html',
#     		form_class = DishForm),
#     	name='dish_edit'),

# # Create a restaurant review, ex.: /myrestaurants/restaurants/1/reviews/create/
# # Unlike the previous patterns, this one is implemented using a method view instead of a class view
#     url(r'\^restaurants/(?P<pk>\\d+)/reviews/create/\$',
#     	'myrestaurants.views.review',
#     	name='review_create'),
# ]

# 	from django.conf.urls import url, include
# from rest_framework import routers
# from rotator.v0.views import (
#     ControlBanner, ControlLibrary, ControlRotator,
#     TrackingRotator, PauseRotator, ActionBanner, AllRotator)

# router = routers.DefaultRouter()

# router.register(r'banner', ControlBanner, base_name='banner')
# router.register(r'library', ControlLibrary, base_name='library')
# router.register(r'rotator', ControlRotator, base_name='rotator')
# router.register(r'track_rotador', TrackingRotator, base_name='track_rotador')
# router.register(
#     r'pause_rotator', PauseRotator, base_name='pause_rotator')
# router.register(
#     r'action_banner', ActionBanner, base_name='action_banner')
# router.register(
#     r'all_rotator', AllRotator, base_name='all_rotator')

# urlpatterns = [
#     url(r'^', include(router.urls)),
#     # url(r'^docs/', include('rest_framework_swagger.urls')),
# ]

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^docs/', include('rest_framework_swagger.urls')),
]
