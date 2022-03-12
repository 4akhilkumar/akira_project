from django.contrib import admin

from .models import (Testing, Block, Floor, Room, Branch, Semester)

admin.site.register(Testing)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Branch)
admin.site.register(Semester)