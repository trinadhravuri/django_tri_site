from django.contrib import admin
from .models import Author,Post,Tag,Comment
# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display = ("title","author")
    list_filter =("author","date","tags")
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name","rating","post")
    list_filter = ("user_name","rating")


admin.site.register(Post,postAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)
