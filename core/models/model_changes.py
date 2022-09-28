from django.db import models
# from . import Review

class ModelYear(models.Model):
    year = models.PositiveIntegerField(null=True, blank=True)
    
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.year)

    class Meta:
	    db_table = "model_year_changes"

        

class BikeClass(models.Model):
    bike_class = models.CharField(max_length=255, null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.bike_class)

    class Meta:
	    db_table = "bike_class_changes"

class FrameType(models.Model):
    frame_type = models.CharField(max_length=255, null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.frame_type)

    class Meta:
	    db_table = "frame_type_changes"


class WheelSize(models.Model):
    wheel_size = models.FloatField(null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.wheel_size)

    class Meta:
	    db_table = "wheel_size_changes"


class BreakType(models.Model):
    break_type = models.CharField(max_length=255, null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.break_type)

    class Meta:
	    db_table = "break_type_changes"