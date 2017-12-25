from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

#taggit 
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

# Create your models here.
def upload_location(instance, filename):
    return "%s %s"%(instance.id, filename)


class PostManager(models.Manager):
    def get_queryset(self):
        pubquery = super(PostManager, self).get_queryset()
        query = pubquery.filter(status='published').filter(publish__lte=timezone.now())
        return query

class Post(models.Model):
    STATUS_CHOICE = (
       ('draft', 'Draft'), 
       ('published', 'Published')
    )
    title    = models.CharField(max_length=50)
    slug     = models.SlugField(max_length=250 , unique_for_date='publish')
    author   = models.ForeignKey(User, related_name='blog_post')
    image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True,
                                height_field = 'height_field',
                                width_field = 'width_field',
                                )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image_info = models.CharField(max_length=30, default='image info', null=True, blank=True)
    content  = models.TextField()

    publish  = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(auto_now=True)
    updated  = models.DateTimeField(auto_now_add=True)
    status   = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    objects = models.Manager()
    tags = TaggableManager()
    publishs = PostManager()

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.publish.year,
                                 self.publish.month,                             
                                 self.publish.day,
                                 self.slug])
    
    def late_post(self):
        #get late post that are after the timezone
        return self.created < self.publish

    def early_post(self):
        #get early post that are before the timezone
        return self.created > self.publish
                                 
from django.db.models.signals import pre_save
from django.utils.text import slugify
  
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
         
def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reciver, sender=Post)
