from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Section, Topic, Message, Notification

# Регистрируем наши модели в админке

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     fieldsets = UserAdmin.fieldsets + (
#         ('Custom Fields', {'fields': ('direction', 'age')}),
#     )

admin.site.register(Section)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Notification)
# admin.site.register(CustomGroup)
# admin.site.register(CustomPermission)




