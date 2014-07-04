from django.conf.urls import patterns, include, url
from tabs.views import IndexView, Tab2View, Tab1View, ThanksView, NameView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',      IndexView.as_view()),
    url(r'^tab1/',  Tab1View.as_view()),
    url(r'^tab2/',  Tab2View.as_view()),
    url(r'^thanks/',ThanksView.as_view()),
    url(r'^names/',  NameView.as_view()),
)
