from django.db import models

# Create your models here.
class Order_db(models.Model):
    symbol=models.CharField(max_length=100,null=True,blank=False)
    Exicuted_p=models.CharField(max_length=100,null=True,blank=False)
    qty=models.CharField(max_length=100,null=True,blank=False)
    order_status=models.CharField(max_length=100,null=True,blank=False)
    Exicuted_orderId=models.CharField(max_length=100,null=True,blank=False)
    profit_Loss_amnt=models.CharField(max_length=100,null=True,blank=False)
    CE_OI=models.CharField(max_length=100,null=True,blank=False)
    PE_OI=models.CharField(max_length=100,null=True,blank=False)

    CE_IV=models.CharField(max_length=100,null=True,blank=False)
    PE_IV=models.CharField(max_length=100,null=True,blank=False)

    CE_VOLM=models.CharField(max_length=100,null=True,blank=False)
    PE_VOLM=models.CharField(max_length=100,null=True,blank=False)
    Date_time=models.CharField(max_length=100,null=True,blank=False)

    Mood=models.CharField(max_length=100,null=True,blank=False)
    Market_condition=models.CharField(max_length=100,null=True,blank=False)
    Preparation=models.CharField(max_length=100,null=True,blank=False)
    Thought=models.CharField(max_length=100,null=True,blank=False)

class Intruction_db(models.Model):
    
    Daily_target=models.CharField(max_length=100,null=True,blank=False)
    weekly_target=models.CharField(max_length=100,null=True,blank=False)
    date_time=models.CharField(max_length=100,null=True,blank=False)
    trading_plans=models.CharField(max_length=100,null=True,blank=False)

class mood_thought_status_db(models.Model):
    
    Mood=models.CharField(max_length=100,null=True,blank=False)
    Market_condition=models.CharField(max_length=100,null=True,blank=False)
    Preparation=models.CharField(max_length=100,null=True,blank=False)
    Thought=models.CharField(max_length=100,null=True,blank=False)
    date_time=models.CharField(max_length=100,null=True,blank=False)
    
    






    
    


    


