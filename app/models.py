from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


# This would add a relation to another model :
# user = models.ForeignKey(
#     User, on_delete=models.SET_NULL, null=True, blank=True
# )
# Then need to run migrations afterwards