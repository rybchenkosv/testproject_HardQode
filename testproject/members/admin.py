from django.contrib import admin
from .models import Product, Lesson, Group, StudentProductAccess

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
admin.site.register(StudentProductAccess)

