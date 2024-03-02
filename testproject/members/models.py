from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_group_size = models.PositiveIntegerField(default=1)
    max_group_size = models.PositiveIntegerField(default=1)
    total_students_with_access = models.IntegerField(default=0, editable=False)


    def __str__(self):
        return self.name

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_link = models.URLField()

    def __str__(self):
        return self.title


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class StudentProductAccess(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    has_access = models.BooleanField(default=False)