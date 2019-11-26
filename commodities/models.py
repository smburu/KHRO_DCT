from django.db import models
import datetime
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from regions.models import StgLocation
from common_info.models import CommonInfo


class StgHealthCommodity(CommonInfo):
    product_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=False,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=500, blank=False, null=False)
    code = models.CharField(unique=True, max_length=50, blank=False, null=False)
    units_of_measure = models.CharField(max_length=200, blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_health_commodity'
        verbose_name = 'Commodity'
        verbose_name_plural = 'Health Commodities'
        ordering = ('name',)

    def __str__(self):
        return self.name #display the indicator name


class FactHealthCommodities(CommonInfo):
    fact_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(StgLocation, models.PROTECT,
        verbose_name = 'Location',)
    product = models.ForeignKey(StgHealthCommodity, models.PROTECT,
        verbose_name = 'Product ID',)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2,
        verbose_name = 'Price',)
    num_of_orders = models.PositiveIntegerField(blank=True, null=True,
        verbose_name = 'Number of Orders',)
    order_quantity = models.IntegerField(blank=True, null=True,
        verbose_name = 'Quantity Ordered',)
    issued_quantity = models.PositiveIntegerField(blank=True, null=True,
        verbose_name = 'Quantity Issued',)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2,
        blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True,
        verbose_name = 'Date Issued')
    comment = models.CharField(max_length=5000, blank=True, null=True)
    public_access = models.CharField(max_length=6,blank=True, null=True,
        default='true',)

    class Meta:
        managed = True
        db_table = 'fact_health_commodities'
        verbose_name = 'Commodities Order'
        verbose_name_plural = 'Commodity Orders'
        ordering = ('product__name','location__name')
        #unique_together = ('product', 'location',) #enforces concatenated unique constraint

    def __str__(self):
         return str(self.product)
