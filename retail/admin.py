from django.contrib import admin
from retail.models import Product, Company

admin.site.register(Product)


@admin.action(description="Очистить задолженность")
def clean_debt(modeladmin, request, queryset):
    queryset.update(debt=0.0)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'supplier', )
    list_filter = ('city',)
    actions = [clean_debt]
