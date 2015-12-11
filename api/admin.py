from django.contrib import admin

# Register your models here.

from .models import User
from .models import Relation
from .models import TalkMsg
from .models import Comment
from .models import Praise
class DeviceAdmin(admin.ModelAdmin):
	fieldsets=[
		#(None,               {'fields': ['question_text']}),
		#('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(User,DeviceAdmin)
admin.site.register(Relation,DeviceAdmin)
admin.site.register(TalkMsg,DeviceAdmin)
admin.site.register(Comment,DeviceAdmin)
admin.site.register(Praise,DeviceAdmin)
