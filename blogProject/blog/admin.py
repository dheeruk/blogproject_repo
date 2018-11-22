from django.contrib import admin
from blog.models import post,commentModel

# Register your models here.
class postAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','update','status']
    prepopulated_fields={'slug':('title',)}
    list_filter=('status','author','created')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=('status','publish')
class commentAdmin(admin.ModelAdmin):
    list_display=['name','email','Post','body','created','updated','active']
    list_filter=('active','created','updated')
    search_fields=('name','email','body')

admin.site.register(post,postAdmin)
admin.site.register(commentModel,commentAdmin)
