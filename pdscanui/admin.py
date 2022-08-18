from django.contrib import admin
from .models import Transmitter
from .models import Receiver
from .models import Measurement
from .models import Data

# make unchangeable object within admin visible
class guiAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'id')


admin.site.register(Transmitter)
admin.site.register(Receiver)
admin.site.register(Measurement, guiAdmin)
admin.site.register(Data)
