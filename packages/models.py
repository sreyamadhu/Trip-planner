from django.db import models

# Create your models here.
class Destination(models.Model):
  spotname=models.CharField(max_length=100)
  spotdistrict=models.CharField(max_length=50)
  location=models.CharField(max_length=100)
  landscape=models.CharField(max_length=100)
  cafespot=models.CharField(max_length=100,blank=True, null=True, default=None)
  description=models.CharField(max_length=1500)
  img=models.ImageField(upload_to='destination')
  latitude=models.CharField(max_length=250)
  longitude=models.CharField(max_length=250)

  def __str__(self):
        return self.spotname
  class Meta:
        ordering = ['id']



class Tourpackage(models.Model):
  MORNING = 'Morning'
  AFTERNOON = 'Afternoon'
  EVENING = 'Evening'

  TIME_CHOICES = [
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    ]
  
  ONEDAYPACKAGE='1daypackage'
  TWODAYPACKAGE='2daypackage'
  THREEDAYPACKAGE='3daypackage'
  FOURDAYPACKAGE='4daypackage'
  FIVEDAYPACKAGE='5daypackage'
  SIXDAYPACKAGE='6daypackage'   
  SEVENDAYPACKAGE='7daypackage'

  CATEGORY_CHOICES=[
       (ONEDAYPACKAGE, '1daypackage'),
       (TWODAYPACKAGE, '2daypackage'),
       (THREEDAYPACKAGE, '3daypackage'),
       (FOURDAYPACKAGE, '4daypackage'),
       (FIVEDAYPACKAGE, '5daypackage'),
       (SIXDAYPACKAGE, '6daypackage'),
       (SEVENDAYPACKAGE, '7daypackage'),

  ]


  id=models.AutoField(primary_key=True)
  packagecategory=models.CharField(max_length=20, choices=CATEGORY_CHOICES)
  district=models.CharField(max_length=50)
  packagenumber=models.PositiveIntegerField()
  daynumber=models.PositiveIntegerField()
  spottime=models.CharField(max_length=20, choices=TIME_CHOICES)
  spotname=models.ForeignKey(Destination, on_delete=models.CASCADE,default=None)
  
  def __str__(self):
        objectname=self.packagecategory+'->'+self.district+str(self.packagenumber)+'->Day '+str(self.daynumber)+'->'+self.spottime+'->'+str(self.spotname)
        return objectname
  
  class Meta:
        db_table_comment = "packages for 7day tour selection"  #for comments
        ordering = ['id']