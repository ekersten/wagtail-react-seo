from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from website.models import Category, Product

class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = "Categories"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)

class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = "Products"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "category")
    search_fields = ("name", "category__name")


class CatalogAdminGroup(ModelAdminGroup):
    menu_label = "Catalog"
    menu_icon = "list-ul"
    menu_order = 200
    items = (CategoryAdmin, ProductAdmin)

modeladmin_register(CatalogAdminGroup)