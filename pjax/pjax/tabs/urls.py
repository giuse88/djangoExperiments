import IndexView from views

urlpatterns = (
    url(r'^$', IndexView.as_view()),
    url(r'^tab1/',  Tab1View.as_view()),
    url(r'^tab2/',  Tab1View.as_view())
    url(r'^name/',  NameView.as_view())
    url(r'^thanks/',ThanksView.as_view())
)
