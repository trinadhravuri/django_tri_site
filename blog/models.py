from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    def fullname(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    def __str__(self):
        return self.fullname()
    
    # class Meta:
    #    verbose_name_plural = "Author"
class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption
     
class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts",null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(50)])
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    comment_text = models.TextField(max_length=1000)
    rating = models.IntegerField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return self.user_name