from django.db import models
from pub.models import params_get
from pub.config.pub_definitions import ParameterType


class Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    address = models.TextField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"


class ActiveBranchManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=ParameterType.PT_Active.value)
    # def active(self, branch_id):
    #     return self.filter(status=ParameterType.PT_Active.value)


class Branch(models.Model):

    def _select_status():
        return params_get(ParameterType.PT_ActivePassive.value)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    address = models.TextField(max_length=100)
    foundation_time = models.DateField()
    status = models.CharField(choices=_select_status, max_length=7)

    objects = models.Manager()
    active = ActiveBranchManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شعبه"
        verbose_name_plural = "شعبه ها"


class AvailableFoodManager(models.Manager):
    
    def filter_by_branch(self, branch_id):
        return self.get_queryset().filter(menu__branch_id=branch_id, menu__is_available=True)


class FoodItem(models.Model):

    def _select_food_category():
        return params_get(ParameterType.PT_FoodCategory.value)

    name = models.CharField(max_length=100)
    category = models.CharField(choices=_select_food_category, max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    objects = models.Manager()
    available_foods = AvailableFoodManager()

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذا ها"


class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.food_item.name} در {self.branch.name}"
    
    class Meta:
        verbose_name = "منو"
        verbose_name_plural = "منو ها"


class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"سفارش {self.id} بوسیله {self.customer.first_name} + ' ' + {self.customer.last_name}"
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"
    
    def calculate_total(self):
        total = sum(item.food_item.price * item.quantity for item in self.items.all())
        return total

    # def save(self, *args, **kwargs):
    #     self.total_price = self.calculate_total()
    #     super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} * {self.food_item.name}"

    class Meta:
        verbose_name = "جزئیات سفارش"
        verbose_name_plural = "جزئیات سفارش ها"
