from django.urls import path

from . import views

# The path() function is passed four arguments,
# two required: route and view
# two optional: kwargs and name
#
# `route` is a string that contains a URL pattern.
# Patterns don't search GET and POST parameters, or the domain name.
#
# `view`: When Django finds a marching pattern,
# it calls the specified view
# function with an HttpRequest object as the first argument and any
# captured values from the route as keyword argument.
#
# `kwargs`: arbitrary keyword arguments can be passed in a dictionary
# to the target view.
#
# `name`: naming URL lets you refer to it unambiguously from elsewhere,
# esp from within templates.

# Set application namespace.
app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    # Angle brackets captures part of the URL and sends it as a
    # keyword argument to the view function.
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]