from django.db import models
import uuid

class Block(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    block_name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return '%s' % (self.block_name)

    class Meta:
        ordering = ['block_name']

class Floor(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    floor_name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return '%s' % (self.floor_name)

    class Meta:
        ordering = ['floor_name']

class Room(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    room_name = models.CharField(max_length = 50, unique = True)
    block = models.ForeignKey(Block, on_delete = models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete = models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return '%s' % (self.room_name)
    
    class Meta:
        ordering = ['room_name']