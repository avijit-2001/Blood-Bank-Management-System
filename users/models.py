from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class CustomUser(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)


class Donor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact = models.IntegerField(default=0000000000)
    age = models.IntegerField(default=0)
    blood_group = models.CharField(max_length=4)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=22)
    pin_code = models.IntegerField(default=000000)
    available = models.BooleanField(default=True)
    # no_accepted = models.IntegerField(default=0)
    # no_rejected = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'


class Hospital(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact = models.IntegerField(default=0000000000)
    registration_id = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=22)
    pin_code = models.IntegerField(default=000000)

    def __str__(self):
        return f'{self.user.username} Hospital'


class Request(models.Model):
    donor_id = models.IntegerField(default=-1)
    hospital_id = models.IntegerField(default=-1)
    blood_group = models.TextField(max_length=4)
    status = models.IntegerField(default=0)
    date_requested = models.DateField(null=True, blank=True)
    date_rejected = models.DateField(null=True, blank=True)
    date_approved = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.hospital_id} to {self.donor_id}'

    # pending = 1
    # accepted = 2
    # rejected = 3
    # approved = 4
    # rejection_viewed = 5


class Reward(models.Model):
    req = models.OneToOneField(Request, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    date_rewarded = models.DateField(null=True, blank=True)


class HospitalRepository(models.Model):
    hospital_user_id = models.IntegerField(default=-1)
    blood_group = models.TextField(max_length=4)
    quantity = models.IntegerField(default=0)
    plasma_count = models.IntegerField(default=10)


class Reason(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    decline_reason = models.TextField(max_length=300)

