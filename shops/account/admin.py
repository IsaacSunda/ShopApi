from django.contrib import admin

from account.models import Payment, Address, Person

# Register your models here.

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Payment)
