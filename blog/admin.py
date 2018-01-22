from django.contrib import admin
from blog import models


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)