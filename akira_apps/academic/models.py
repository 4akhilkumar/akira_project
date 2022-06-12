from django.db import models
from django.contrib.auth.models import User

import uuid

def ordinal(n):
    s = ('th', 'st', 'nd', 'rd') + ('th',)*10
    v = n%100
    if v > 13:
        return f'{n}{s[v%10]}'
    else:
        return f'{n}{s[v]}'

def returnFloorName(floorName):
    if floorName.isnumeric():
        floorName = ordinal(int(floorName)) + " Floor"
    if any(char.isdigit() for char in floorName):
        for i, char in enumerate(floorName):
            if char.isdigit():
                floorName = ordinal(int(floorName[i])) + " Floor"
                break
    return floorName

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

class BlockExtraFields(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    field_name = models.CharField(max_length = 100)
    field_type = models.CharField(max_length = 100)
    field_value = models.TextField(max_length = 50000)

    def __str__(self):
        return '%s - %s' % (self.block, self.field_name)

class Floor(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

    def save(self, *args, **kwargs):
        self.name = returnFloorName(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'block']

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
        unique_together = ['block', 'floor', 'name']

class Branch(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique = True)
    description = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['name']