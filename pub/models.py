from django.db import models


class Parameters(models.Model):

    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    type = models.IntegerField()
    order_no = models.IntegerField(default=1)
    description = models.CharField(max_length=250)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پارامترهای عمومی"
        verbose_name_plural = "پارامترهای عمومی"

    def __str__(self):
        return self.name

def params_get(type):
    items = Parameters.objects.filter(type=type, parent__isnull = False)
    return [(r.code, r.name) for r in items]