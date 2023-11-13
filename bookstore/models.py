from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=1024, null=True,blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(blank=True,default='user_img.png',upload_to='profile_images')

    def __str__(self) :
        return f"{self.user}"
    
class Tag(models.Model):
    name = models.CharField(max_length=15)
    
    
    def __str__ (self):
        return  self.name
    
   
class Book(models.Model):
    CATEGORY = (('Fiction','Fiction'),
              ('Historical Fiction','Historical Fiction'),
              ('Mystery','Mystery'),
              ('Fantasy','Fantasy'),
              ('Horror','Horror'),)
    
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100, choices=CATEGORY)
    description = models.TextField(max_length=1024)
    tag = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        tags = ', '.join(tag.name for tag in self.tag.all())
        return self.name
    

class Order(models.Model):

    STATUS = (('Pending','Pending'),
              ('Delivered','Delivered'),
              ('In Progress','In Progress'),
              ('Out of order','Out of order'))
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # tag = models.ManyToManyField(Tag)
    
    
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)
    def __str__(self):
        return self.status
    