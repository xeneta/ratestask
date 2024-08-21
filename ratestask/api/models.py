from django.db import models


class Region(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    parent_slug = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subregions', db_column='parent_slug')

    class Meta:
        db_table = 'regions'
        ordering = ['name'] 

    def __str__(self):
        return self.name

class Port(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=255)
    parent_slug = models.ForeignKey(Region, on_delete=models.CASCADE, to_field='slug', related_name='ports', db_column='parent_slug')

    class Meta:
        db_table = 'ports'

    def __str__(self):
        return self.name

class Price(models.Model):
    id = models.AutoField(primary_key=True)
    orig_code = models.ForeignKey(Port, related_name='origin_prices', on_delete=models.CASCADE, to_field='code', db_column='orig_code')
    dest_code = models.ForeignKey(Port, related_name='destination_prices', on_delete=models.CASCADE, to_field='code', db_column='dest_code')
    day = models.DateField()
    price = models.IntegerField()

    class Meta:
        db_table = 'prices'

    def __str__(self):
        return f"Price from {self.orig_code} to {self.dest_code} on {self.day}"
 