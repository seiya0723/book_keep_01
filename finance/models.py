from django.db import models
from django.utils import timezone

class Category(models.Model):

    class Meta:
        db_table = "category"

    name    = models.CharField(verbose_name="カテゴリ名",max_length=20)
    income  = models.BooleanField(verbose_name="収入フラグ",default=False)
    
    def __str__(self):
        return self.name


class Balance(models.Model):

    class Meta:
        db_table = "balance"

    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    pay_dt      = models.DateField(verbose_name="決済日")
    category    = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.PROTECT)
    value       = models.IntegerField(verbose_name="金額")

    def __str__(self):
        return self.category.name



