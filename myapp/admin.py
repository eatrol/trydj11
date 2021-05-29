from django.contrib import admin
from myapp.models import *

# Register your models here.

class ericproAdmin(admin.ModelAdmin):
 	list_display=('id','name','cata','subcata','isnew','isprice','price','image','stock','image1','image2','image3','description')


class ericorderAdmin(admin.ModelAdmin):
 	list_display=('id','name','accept','status','price','shoplist','shopqty','shopprice','cName','cPhone','cAddress','cMail','tradeinfo','tradesha256')


class ericuserAdmin(admin.ModelAdmin):
 	list_display=('id','name','userid','password','score','data')


admin.site.register(ericpro,ericproAdmin)
admin.site.register(ericorder,ericorderAdmin)
admin.site.register(ericuser,ericuserAdmin)
#admin.site.register(Order,OrderAdmin)