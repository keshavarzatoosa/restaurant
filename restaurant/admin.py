from django.contrib import admin
from .models import *
from .forms import MenuForm, OrderForm


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 # -- تعداد فرم های خالی پیش فرض
    # can_delete = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'food_item':
            order_id = request.resolver_match.kwargs.get('object_id')
            if order_id:
                order = Order.objects.get(id=order_id)
                branch_id = order.branch.id
                kwargs['queryset'] = FoodItem.available_foods.filter_by_branch(branch_id)
            else:
                kwargs['queryset'] = FoodItem.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('id', 'customer', 'branch', 'order_time')
    inlines = [OrderItemInline]


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'phone', 'address')

    # def get_queryset(self, request):
    #     return Branch.active.all()


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'address')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'branch', 'is_available')
    form = MenuForm

admin.site.register(Customers, CustomersAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Menu, MenuAdmin)