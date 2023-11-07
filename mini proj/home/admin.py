from django.contrib import admin
from .models import CustomUser
from .models import MigratoryWorker
from .models import WorkCategory



admin.site.register(CustomUser)
admin.site.register(MigratoryWorker)
admin.site.register(WorkCategory)

