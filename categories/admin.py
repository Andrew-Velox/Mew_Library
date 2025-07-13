from django.contrib import admin
from .models import BookCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

admin.site.register(BookCategory,CategoryAdmin)