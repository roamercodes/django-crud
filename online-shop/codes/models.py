from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	profile_pic = models.ImageField(default='fotokosong.gif', blank=True)

	def __str__(self):
		return self.name

def save(self):
    super().save()
    img = Image.open(self.profile_pic.path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.profile_pic.path)

class Tag(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
 CATEGORY=(
 ('Indoor', 'Indoor'),
 ('Out Door' , 'Out Door'),
 )
 name = models.CharField(max_length=200, blank=True, null=True)
 price = models.IntegerField(blank=True, null=True)
 category = models.CharField(max_length=200, blank=True, null=True, choices=CATEGORY)
 description = models.CharField(max_length=200, blank=True, null=True)
 date_created= models.DateTimeField(auto_now_add=True, null=True)
 tag = models.ManyToManyField(Tag)

 def __str__(self):
     return self.name
class Order(models.Model):
 STATUS=(
 ('Pending', 'Pending'),
 ('Out for delivery' , 'Out for delivery'),
 ('Delivered', 'Delivered'),
 )
 customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
 product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
 date_created = models.DateTimeField(auto_now_add=True, null=True)
 status = models.CharField(max_length=200, null=True, choices=STATUS)
 note = models.CharField(max_length=200, blank=True, null=True)

 def __str__(self):
     return self.product.name