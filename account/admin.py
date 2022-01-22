from django.contrib import admin
from account.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined")


admin.site.register(Account, AccountAdmin)
