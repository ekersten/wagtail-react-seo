from django.db import models
from django.http import Http404

from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from django_extensions.db.fields import AutoSlugField
from wagtailmetadata.models import MetadataPageMixin, MetadataMixin

class WebsitePage(MetadataPageMixin, Page):
    pass


class CatalogPage(MetadataPageMixin, RoutablePageMixin, Page):
    @path("")
    def index(self, request):
        categories = Category.objects.all()
        return self.render(request, context_overrides={
            "seo_object": self,
            "categories": categories,
        })

    @path("category/<slug:category_slug>/")
    def category(self, request, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
            return self.render(request, context_overrides={
                "seo_object": category
            })
        except Category.DoesNotExist:
            return Http404
    
    @path("product/<slug:product_slug>/")
    def product(self, request, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            return self.render(request, context_overrides={
                "seo_object": product
            })
        except Product.DoesNotExist:
            return Http404


class Category(MetadataMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True, overwrite=True)

    def get_meta_url(self):
        page = CatalogPage.objects.first()
        return page.reverse_subpage("category", kwargs={"category_slug": self.slug})
    
    def get_meta_title(self):
        page = CatalogPage.objects.first()
        return f'{self.name} | {page.title}'

    def get_meta_description(self):
        return f'All products in {self.name} category'

    def __str__(self):
        return self.name
    


class Product(MetadataMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True, overwrite=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_meta_url(self):
        page = CatalogPage.objects.first()
        return page.reverse_subpage("product", kwargs={"product_slug": self.slug})
    
    def get_meta_title(self):
        page = CatalogPage.objects.first()
        return f'{self.name} | {page.title}'

    def get_meta_description(self):
        return f'Product {self.name}'

    def __str__(self):
        return self.name