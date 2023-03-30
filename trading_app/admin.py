from django.contrib import admin

from trading_app.models import Order_db
from trading_app.models import Intruction_db
from trading_app.models import mood_thought_status_db

 

admin.site.register(Order_db)
admin.site.register(Intruction_db)
admin.site.register(mood_thought_status_db)





# Register your models here.