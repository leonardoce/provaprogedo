from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    """
    This model represent a category of posts
    """
    title = models.CharField(max_length=512, null=False)
    slug = models.SlugField(null=False, unique=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the model, which is used in the
        Django Admin interface
        """
        return "Category: %s" % self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category', kwargs={'slug': str(self.slug)})

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    """
    This model represent a post of the blog
    """
    title = models.CharField(max_length=1024, null=False)
    slug = models.SlugField(null=False, unique=True, max_length=255)
    category = models.ForeignKey('Category')
    content = models.TextField(null=False)
    date = models.DateField()
    author = models.ForeignKey('auth.User')
    is_published = models.BooleanField()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post', kwargs={'slug': str(self.slug)})

    @property
    def excerpt(self):
        return self.content[:100] + "..."

    def __str__(self):
        """
        Returns the string representation of the model, which is used in the
        Django Admin interface
        """
        return "Post: %s" % self.title


class Comment(models.Model):
    """
    This model represent a comment on a post
    """
    content = models.TextField()
    author = models.ForeignKey('auth.User')
    date = models.DateField()
    post = models.ForeignKey('Post')

    def __str__(self):
        """
        Returns the string representation of this comment
        """
        return "Comment on post %s with ID %s" % (self.post.title, self.id)

    @property
    def gravatar_url(self):
        """
        Returns the gravatar URL for this user
        """
        import hashlib
        m = hashlib.md5()
        m.update(self.author.email.encode())
        return "https://www.gravatar.com/avatar/" + m.hexdigest()
