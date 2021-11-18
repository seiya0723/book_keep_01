from django.contrib import admin

from .models import Category,Balance


class BalanceAdmin(admin.ModelAdmin):

    list_display    = [ "category","dt","pay_dt","value" ]


admin.site.register(Category)
admin.site.register(Balance,BalanceAdmin)

