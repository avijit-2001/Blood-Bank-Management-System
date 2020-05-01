from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(Request)
admin.site.register(Reward)
admin.site.register(HospitalRepository)
admin.site.register(Reason)
