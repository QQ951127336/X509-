from django.contrib import admin
from .models import User
from .models import Key
from .models import CerApply
from .models import Certificate
from .models import ApplyForRevok,Revoke
# Register your models here.
admin.site.register(User)
admin.site.register(Key)
admin.site.register(CerApply)
admin.site.register(Certificate)
admin.site.register(ApplyForRevok)
admin.site.register(Revoke)