from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category',  kwargs={'cat_name':self.title})


class Provider(models.Model):
    title = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Manufact(models.Model):
    title = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=30, default='Prod')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(max_length=50)
    remain_in_stock = models.IntegerField()
    amount_ordered = models.IntegerField()
    ordered_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={"product_id":self.pk})


class TechProduct(Product):
    weight = models.FloatField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    manuf = models.ForeignKey(Manufact, on_delete=models.CASCADE)


class Videocard(TechProduct):
    freq = models.IntegerField()
    v_memory = models.IntegerField()
    memory_type = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Proccessor(TechProduct):
    freq = models.IntegerField()
    socket = models.CharField(max_length=30)
    c_memory = models.IntegerField()

    def __str__(self):
        return self.title


class Memory(TechProduct):
    size = models.IntegerField()
    mem_type = models.IntegerField()

    def __str__(self):
        return self.title


class Computer(Product):
    gabs = models.CharField(max_length=30)
    manuf = models.ForeignKey(Manufact, on_delete=models.CASCADE)
    videocard = models.ForeignKey(Videocard, on_delete=models.CASCADE)
    processor = models.ForeignKey(Proccessor, on_delete=models.CASCADE)
    memory_p = models.ForeignKey(Memory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Transport(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Users_order(models.Model):
    users_fio = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50)
    users_products = models.ManyToManyField(Product, blank=False)
    users_address = models.CharField(max_length=100, blank=True, null=True)
    dest_type = models.ForeignKey(Transport, blank=False,  null=True, on_delete=models.CASCADE)
    full_price = models.IntegerField()


