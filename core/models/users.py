from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):

        """create a new user and super user in model"""

        account = self.model(
            email=self.normalize_email(email),
            # username=kwargs.get("username")
        )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.is_admin = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """

    LOGIN_TYPE = (
        ("EMAIL", _("EMAIL")),
        ("GOOGLE", _("GOOGLE")),
        ("Facebook", _("Facebook")),
        ("Twitter", _("Twitter")),
    )
    email = models.EmailField(null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=80, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_image",
        null=True,
        blank=True,
        verbose_name=_("Profile Image"),
    )
    password = models.CharField(max_length=255, null=True)
    login_type = models.CharField(max_length=50, choices=LOGIN_TYPE, default="EMAIL")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        db_table = "users"


class ReviewCSV1(models.Model):
    URL = models.TextField(null=True, blank=True)
    Year = models.TextField(null=True, blank=True)
    Brand = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Trim = models.TextField(null=True, blank=True)
    MSRP = models.TextField(null=True, blank=True)
    Class = models.TextField(null=True, blank=True)
    Frame_Type = models.TextField(null=True, blank=True)
    Frame = models.TextField(null=True, blank=True)
    Weight = models.TextField(null=True, blank=True)
    Load_Capacity = models.TextField(null=True, blank=True)
    Suspension = models.TextField(null=True, blank=True)
    Fork = models.TextField(null=True, blank=True)
    Rear_Shock = models.TextField(null=True, blank=True)
    Wheel_Size = models.TextField(null=True, blank=True)
    Front_Wheel = models.TextField(null=True, blank=True)
    Rear_Wheel = models.TextField(null=True, blank=True)
    Front_Hub = models.TextField(null=True, blank=True)
    Rear_Hub = models.TextField(null=True, blank=True)
    Tires = models.TextField(null=True, blank=True)
    Gears = models.TextField(null=True, blank=True)
    Shift_Levers = models.TextField(null=True, blank=True)
    Front_Derailleur = models.TextField(null=True, blank=True)
    Crankset = models.TextField(null=True, blank=True)
    Rear_Derailleur = models.TextField(null=True, blank=True)
    Electronic_Shifting = models.TextField(null=True, blank=True)
    Internally_Geared_Hub = models.TextField(null=True, blank=True)
    Continually_Variable_Transmission = models.TextField(null=True, blank=True)
    Cassette = models.TextField(null=True, blank=True)
    Chainring = models.TextField(null=True, blank=True)
    Belt_Drive = models.TextField(null=True, blank=True)
    Headset = models.TextField(null=True, blank=True)
    Stem = models.TextField(null=True, blank=True)
    Handlebar = models.TextField(null=True, blank=True)
    Grips = models.TextField(null=True, blank=True)
    Seatpost = models.TextField(null=True, blank=True)
    Seatpost_Diameter = models.TextField(null=True, blank=True)
    Saddle = models.TextField(null=True, blank=True)
    Pedals = models.TextField(null=True, blank=True)
    Brake_Type = models.TextField(null=True, blank=True)
    Front_Brake = models.TextField(null=True, blank=True)
    Rear_Brake = models.TextField(null=True, blank=True)
    Motor_Type = models.TextField(null=True, blank=True)
    Motor = models.TextField(null=True, blank=True)
    Additional_Motors = models.TextField(null=True, blank=True)
    Motor_Nominal_Output = models.TextField(null=True, blank=True)
    Display = models.TextField(null=True, blank=True)
    Smart_Bike = models.TextField(null=True, blank=True)
    Theft_GPS = models.TextField(null=True, blank=True)
    Additional_Battery = models.TextField(null=True, blank=True)
    Battery_Watt_Hrs = models.TextField(null=True, blank=True)
    Battery = models.TextField(null=True, blank=True)
    Charger = models.TextField(null=True, blank=True)
    Lights = models.TextField(null=True, blank=True)
    Fenders = models.TextField(null=True, blank=True)
    Front_Rack = models.TextField(null=True, blank=True)
    Rear_Rack = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "review_csv_1"


class ReviewCSV2(models.Model):
    URL = models.TextField( null=True, blank=True)
    Cruiser = models.TextField( null=True, blank=True)
    City = models.TextField( null=True, blank=True)
    Commuting = models.TextField( null=True, blank=True)
    Folding = models.TextField( null=True, blank=True)
    Fat = models.TextField( null=True, blank=True)
    Hunting = models.TextField( null=True, blank=True)
    All_Other_Fat = models.TextField( null=True, blank=True)
    Mountain = models.TextField( null=True, blank=True)
    Cross_Country = models.TextField( null=True, blank=True)
    Trail = models.TextField( null=True, blank=True)
    All_Mountain_Enduro = models.TextField( null=True, blank=True)
    Freeride_Downhill = models.TextField( null=True, blank=True)
    All_Other_Mountain = models.TextField( null=True, blank=True)
    Cargo = models.TextField( null=True, blank=True)
    Utility = models.TextField( null=True, blank=True)
    Box_Bike = models.TextField( null=True, blank=True)
    All_Other_Cargo = models.TextField( null=True, blank=True)
    Road = models.TextField( null=True, blank=True)
    Drop_Bars = models.TextField( null=True, blank=True)
    Gravel = models.TextField( null=True, blank=True)
    All_Other_Road = models.TextField( null=True, blank=True)
    Trike = models.TextField( null=True, blank=True)
    Delta = models.TextField( null=True, blank=True)
    Tadpole = models.TextField( null=True, blank=True)
    All_Other_Trike = models.TextField( null=True, blank=True)
    Recumbent = models.TextField( null=True, blank=True)
    Minibike = models.TextField( null=True, blank=True)
    Kids = models.TextField( null=True, blank=True)
    Other = models.TextField( null=True, blank=True)

    class Meta:
        verbose_name = "review_csv_2"


class ReviewCSV3(models.Model):
    URL = models.TextField( null=True, blank=True)
    Suggested_Use = models.TextField( null=True, blank=True)
    Warranty = models.TextField( null=True, blank=True)
    Availability = models.TextField( null=True, blank=True)
    Battery_Weight = models.TextField( null=True, blank=True)
    Motor_Weight = models.TextField( null=True, blank=True)
    Frame_Sizes = models.TextField( null=True, blank=True)
    Geometry_Measurements = models.TextField( null=True, blank=True)
    Frame_Colors = models.TextField( null=True, blank=True)
    Attachment_Points = models.TextField( null=True, blank=True)
    Brake_Details = models.TextField( null=True, blank=True)
    Seatpost_Length = models.TextField( null=True, blank=True)
    Spokes = models.TextField( null=True, blank=True)
    Tire_Details = models.TextField( null=True, blank=True)
    Tube_Details = models.TextField( null=True, blank=True)
    Accessories = models.TextField( null=True, blank=True)
    Other = models.TextField( null=True, blank=True)
    Motor_Output_Peak = models.TextField( null=True, blank=True)
    Motor_Torque = models.TextField( null=True, blank=True)
    Battery_Chemistry = models.TextField( null=True, blank=True)
    Charge_Time = models.TextField( null=True, blank=True)
    Estimated_Min_Range = models.TextField( null=True, blank=True)
    Estimated_Max_Range = models.TextField( null=True, blank=True)
    Display_Readouts = models.TextField( null=True, blank=True)
    Display_Accessories = models.TextField( null=True, blank=True)
    Drive_Mode = models.TextField( null=True, blank=True)
    Drive_Mode_Details = models.TextField( null=True, blank=True)
    Top_Speed = models.TextField( null=True, blank=True)

    class Meta:
        verbose_name = "review_csv_3"
