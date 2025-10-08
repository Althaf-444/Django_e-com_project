from django.db import models
from store.models import Product , Variation
from category.models import Category
from accounts.models import Account
from django.urls import reverse

# Create your models here.

class Cart(models.Model):
    cart_id     = models.CharField(max_length=250 , blank=True)
    date_added  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user         = models.ForeignKey(Account , on_delete = models.CASCADE , null=True)
    product      = models.ForeignKey(Product , on_delete=models.CASCADE)
    variations   = models.ManyToManyField(Variation , blank= True)
    cart         = models.ForeignKey(Cart , on_delete=models.CASCADE , null = True)
    quantity     = models.IntegerField()
    is_active    = models.BooleanField(default=True)


    def sub_total(self):
        return (self.product.price * self.quantity)
       
    def get_url(self):
        return reverse("product_details", args=[self.category.slug , self.slug,])
    

    def __unicode__(self):
         # Shows product name + variations
        variation_values = ", ".join([v.variation_value for v in self.variations.all()])
        return f"{self.product.product_name} ({variation_values})"