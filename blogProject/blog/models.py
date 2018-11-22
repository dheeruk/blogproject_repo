from django.db import models
from django.utils import timezone
from django.contrib.auth.models  import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

# Create your models here.
class custmodel_manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class post(models.Model):
    status=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=status,default='draft')
    objects=custmodel_manager()
    tags=TaggableManager()
    class Meta:
        ordering=('-publish',)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
class commentModel(models.Model):
    Post=models.ForeignKey(post,related_name='comments')
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)
        def __str__(self):
            return 'comment By {} on {}'.format(self.name,self.Post)
