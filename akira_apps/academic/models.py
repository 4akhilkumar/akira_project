from django.db import models
from django.contrib.auth.models import User
import uuid

class Academy(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length = 10, unique = True)
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)

    def __str__(self):
        return '%s - %s' % (self.code, self.name)

class Block(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique = True)
    desc = models.CharField(max_length = 100, blank = True, null = True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']

class Floor(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'block')

class Room(models.Model):
    TYPE = [
        ('Class Room', 'Class Room'),
        ('Staff Room', 'Staff Room'),
        ('Laboratory', 'Laboratory'),
        ('Activity Room', 'Activity Room'),
        ('Meeting Hall', 'Meeting Hall'),
        ('Waiting Hall', 'Waiting Hall'),
        ('Other','Other'),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete = models.CASCADE)
    type = models.CharField(max_length = 15, choices = TYPE, default = 1)
    capacity = models.IntegerField()

    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['name']
        unique_together = ('block', 'floor', 'name')

class Branch(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['name']

class Semester(models.Model):
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    mode = models.CharField(max_length = 4, choices = MODE, default = 1)
    start_year = models.DateField()
    end_year = models.DateField()
    branch = models.ManyToManyField(Branch)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.mode, self.start_year.year)

    class Meta:
        ordering = ['-start_year']

# Testing Many-to-Many
class Testing(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Block)