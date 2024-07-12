from django.contrib import admin

from roster.models import Task, Tag, User, Occupation


admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Occupation)
