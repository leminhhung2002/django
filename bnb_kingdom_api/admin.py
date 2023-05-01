from django.contrib import admin
from . import models
class PayInterestAdmin(admin.ModelAdmin):
    list_display= ('id','wallet_address',
    'interest_introduced', 
    'interest_package', 
    'timeProccess',
    'created_at',
    'date_created')

class IntroductionAdmin(admin.ModelAdmin):
    list_display= ( 'id',
    'wallet_address',
    'wallet_address_introduced',
    'F_ratings',
    'created_at' ,
    'date_created')
class BuyHistoryAdmin(admin.ModelAdmin):
    list_display= (
    'id',
    'user',
    'uid',
    'buy_history_id',
    'created_at',
    'date_created',
    'amount_bnb',
    'package_selected',
    'is_complete',
    'note')

class UserAdmin(admin.ModelAdmin):
    list_display= (
    'id',
    'user_id',
    'created_at',
    'date_created',
    'wallet_address'
    )


# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.BuyHistory, BuyHistoryAdmin)
admin.site.register(models.Introduction, IntroductionAdmin)
admin.site.register(models.PayInterest, PayInterestAdmin)