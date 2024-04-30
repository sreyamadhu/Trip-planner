from django.db import models
from packages.models import Destination
from users.models import CustomUser
# Create your models here.
class Review(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  spotname=models.ForeignKey(Destination,on_delete=models.CASCADE)
  spotdistrict = models.CharField(max_length=50)
  content=models.CharField(max_length=1500)
  review_image1 = models.ImageField(upload_to='review_images/', blank=True, null=True, default=None)
  review_image2 = models.ImageField(upload_to='review_images/', blank=True, null=True, default=None)

  def __str__(self):
        objectname=str(self.id)+"->"+str(self.user)+'->'+self.spotdistrict+'->'+str(self.spotname)
        return objectname
  
class Newspot(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  spotname=models.CharField(max_length=100)
  district = models.CharField(max_length=50)
  location = models.CharField(max_length=100)
  description=models.CharField(max_length=1500)
  new_spot_image1 = models.ImageField(upload_to='new_spot_images/',blank=True, null=True, default=None)
  new_spot_image2 = models.ImageField(upload_to='new_spot_images/', blank=True, null=True, default=None)
  new_spot_image3 = models.ImageField(upload_to='new_spot_images/', blank=True, null=True, default=None)

  def __str__(self):
        objectname=str(self.id)+"->"+str(self.user)+'->'+self.spotname+'->'+self.district+'->'+self.location
        return objectname