from django.db import models
import uuid

BRANCH_CHOICES = [
    ("","Branch Name"),
    ("Computer Science and Engineering","Computer Science and Engineering"),
    ("Aerospace/aeronautical Engineering","Aerospace/aeronautical Engineering"),
    ("Chemical Engineering","Chemical Engineering"),
    ("Civil Engineering","Civil Engineering"),
    ("Electronics and Communications Engineering","Electronics and Communications Engineering"),
    ("Electrical and Electronics Engineering","Electrical and Electronics Engineering"),
    ("Petroleum Engineering","Petroleum Engineering"),
    ("Bio Technology","Bio Technology"),
    ("Mechanical Engineering","Mechanical Engineering"),
]

class Block(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    block_name = models.CharField(max_length = 50, unique = True)
    block_desc = models.CharField(max_length = 100, blank = True, null = True)

    def __str__(self):
        return '%s' % (self.block_name)

    class Meta:
        ordering = ['block_name']

class Floor(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    floor_name = models.CharField(max_length = 50)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)

    def __str__(self):
        return '%s' % (self.floor_name)

    class Meta:
        ordering = ['floor_name']
        unique_together = ('floor_name', 'block')

class Room(models.Model):
    TYPE = [
        ('Class Room','Class Room'),
        ('Staff Room','Staff Room'),
        ('Lab','Lab'),
        ('Meeting Hall','Meeting Hall'),
        ('Waiting Hall','Waiting Hall'),
        ('Other','Other'),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    room_name = models.CharField(max_length = 50)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete = models.CASCADE)
    type = models.CharField(max_length = 15, choices = TYPE, default = 1)
    capacity = models.IntegerField()

    def __str__(self):
        return '%s' % (self.room_name)
    
    class Meta:
        ordering = ['room_name']
        unique_together = ('block', 'floor', 'room_name')

class Semester(models.Model):
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    mode = models.CharField(max_length = 4, choices = MODE, default = 1)
    start_year = models.DateField()
    end_year = models.DateField()
    branch = models.CharField(max_length = 50, choices = BRANCH_CHOICES, default=1)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.mode, self.start_year.year)

    class Meta:
        ordering = ['-start_year']