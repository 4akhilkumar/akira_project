from django import template
register = template.Library()
from ..models import (Floor, Room)

@register.filter
def block_floors(value):
    getFloors = Floor.objects.filter(block__block_name=value).count()
    return getFloors

@register.filter
def block_rooms(value):
    getRooms = Room.objects.filter(block__block_name=value).count()
    return getRooms

@register.filter
def block_waiting_halls(value):
    getBlockWaitingHalls = Room.objects.filter(block__block_name=value, type="Waiting Hall").count()
    return getBlockWaitingHalls

@register.filter
def block_lab_rooms(value):
    getBlockLabRooms = Room.objects.filter(block__block_name=value, type="Lab").count()
    return getBlockLabRooms

@register.filter
def block_staff_rooms(value):
    getBlockStaffRooms = Room.objects.filter(block__block_name=value, type="Staff Room").count()
    return getBlockStaffRooms

@register.filter
def block_class_rooms(value):
    getBlockClassRooms = Room.objects.filter(block__block_name=value, type="Class Room").count()
    return getBlockClassRooms

@register.filter
def block_meeting_halls(value):
    getBlockMeetingHalls = Room.objects.filter(block__block_name=value, type="Meeting Hall").count()
    return getBlockMeetingHalls