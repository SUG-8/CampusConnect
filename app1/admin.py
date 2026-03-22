from django.contrib import admin
from .models import TimeSlot, Booking, AddOn, AvailableDate, CourseSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("time", "is_active")
    list_filter = ("is_active",)


admin.site.register(Booking)
admin.site.register(AddOn)
admin.site.register(AvailableDate)
admin.site.register(CourseSlot)
