from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
# Create your models here.

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
            ordering = ('category_name',)

    def __str__(self):
        return self.category_namecategory

    def get_absolute_url(self):
        return f'/{self.slug}/'

class StoreProductsModel(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    images = models.ImageField(upload_to = "uploads/",blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    is_avaible = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'
    
    def get_image(self):
        if self.images:
            return "http://127.0.0.1:8000" + self.images.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url
        else:
            if self.images:
                self.thumbnail = self.make_thumbnail(self.images)
                self.save()

                return "http://127.0.0.1:8000" + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image , size = (300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality = 85)

        thumbnail = File(thumb_io, name = image.name)
        return thumbnail

    