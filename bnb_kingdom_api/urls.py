from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("get_user/<str:wallet_address>",
         views.get_user, name="get_user"),
    path("get_buy_history/<str:wallet_address>",
         views.get_buy_history, name="get_buy_history"),
    path("register_user/", views.register_user, name="register_user"),
    path("save_buy_history/", views.save_buy_history, name="save_buy_history"),
    path("show_person_below_introduced/", views.show_person_below_introduced, name="show_person_below_introduced"),
    path("introduce/<str:wallet_address>/<str:wallet_address_introduced>", views.introduce, name="introduce"),
    path("auto_pay_interest/<str:wallet_address>", views.auto_pay_interest, name="introduce"),



]
