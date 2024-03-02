from django.contrib import admin
from .models import user,resultHistory,userFeedback

admin.site.register(user)
admin.site.register(resultHistory)
admin.site.register(userFeedback)