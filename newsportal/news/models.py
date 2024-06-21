from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        posts_by = Post.objects.filter(author=self.pk)
        post_rating = 0
        comments_rating = 0
        for post in posts_by:
            post_rating += post.rating

            for comment in Comment.objects.filter(post=post.pk):
                comments_rating += comment.rating

        for comment in Comment.objects.filter(author=self.pk):
            comments_rating += comment.rating

        self.rating += (post_rating * 3) + comments_rating


class Category(models.Model):
    cat_name = models.CharField(max_length=64, unique=True)

class Post(models.Model):
    article = "ar"
    news = "nw"
    PostTypes = [(article, "Article"), (news, "News")]
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="authors")
    post_type = models.CharField(max_length=2, choices=PostTypes, default=news)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=64)
    content = models.TextField()
    rating = models.FloatField(default=0.0)

    def preview(self)-> str:
        return self.content[:124] + "..."

    def like(self):
        self.rating += 1.0
        self.save()

    def dislike(self):
        self.rating -= 1.0
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    content = models.TextField(max_length=500)

    def like(self):
        self.rating += 1.0
        self.save()

    def dislike(self):
        self.rating -= 1.0
        self.save()

