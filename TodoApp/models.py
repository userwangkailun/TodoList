from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.EmailField()


class TodoList(models.Model):
	user = models.CharField(max_length = 50)
	title = models.CharField(max_length = 50)
	todo = models.CharField(max_length = 200)
	create_time = models.DateTimeField(auto_now_add=True)

