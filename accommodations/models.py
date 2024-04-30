from django.db import models
from users.models import CustomUser
# Create your models here.
class Accommodationdetailstable(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    lowest_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    highest_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    restaurant = models.BooleanField(blank=True, null=True, default=False)
    accommodation_image1 = models.ImageField(upload_to='accommodation_images/', blank=True, null=True, default=None)
    accommodation_image2 = models.ImageField(upload_to='accommodation_images/', blank=True, null=True, default=None)

    def __str__(self):
        return self.name