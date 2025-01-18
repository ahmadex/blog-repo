from django.contrib import admin
from blog_post.models import BlogUser, BlogPost, Reaction
# Register your models here.


admin.site.register(BlogUser)
admin.site.register(BlogPost)
admin.site.register(Reaction)

