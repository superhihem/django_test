from django.urls import path



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("trades", views.trades, name="trades"),
    path("trades/<int:id>", views.trades, name="trades"),
    path("trades/<int:trade_id>/images/", views.trade_images, name="trade_images"),
    path("trades/<int:trade_id>/images/<int:image_id>", views.trade_images, name="trade_images"),
]