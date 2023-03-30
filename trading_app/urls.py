from django.urls import path
from.import views

urlpatterns=[
  #python  path("",views.store,name="store"),
    # path("",views.trading,name="trading"),
    path("symbol_token_data",views.symbol_token_data,name='symbol_token_data'),
    path("round_nearest",views.round_nearest,name='round_nearest'),
    path("",views.nifty_option_data,name='nifty_option_data'),
    path('expiry_date_dropdwn',views.expiry_date_dropdwn,name="expiry_date_dropdwn"),
    path('option_data_refresh',views.option_data_refresh,name="option_data_refresh"),
    path('NIFTY_CE_buy',views.NIFTY_CE_buy,name="NIFTY_CE_buy"),
    path("NIFTY_PE_buy",views.NIFTY_PE_buy,name="NIFTY_PE_buy"),
    path("square_off",views.square_off,name="square_off"),
    path("instructions",views.instructions,name="instructions"),
    path("instru_data_post",views.instru_data_post,name="instru_data_post"),
    path("mood_thought_data_post",views.mood_thought_data_post,name="mood_thought_data_post"),
    path("order_data",views.order_data,name="order_data"),

]