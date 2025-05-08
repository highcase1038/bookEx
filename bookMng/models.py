from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import os


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # First save the model to get an ID and process the image
        super().save(*args, **kwargs)

        # Update pic_path based on the picture field if picture exists
        if self.picture and hasattr(self.picture, 'url'):
            # Strip leading '/media/' from the URL path if present
            url_path = self.picture.url
            if url_path.startswith('/media/'):
                self.pic_path = url_path[7:]  # Remove '/media/' prefix
            else:
                self.pic_path = url_path

            # If changes were made to pic_path, save again
            if self._state.adding is False:  # Only save again if not a new object
                super().save(update_fields=['pic_path'])

    @property
    def get_image_url(self):
        """Return the image URL or placeholder if no image exists"""
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        return '/static/placeholder-book.png'  # Default placeholder path

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"Rating: {self.score} by {self.user.username} for {self.book.name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.book.name}"

class BookRequest(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        created_date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.title

        def get_like_count(self):
            return self.requestlike_set.count()

class RequestLike(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        book_request = models.ForeignKey('BookRequest',
                                         on_delete=models.CASCADE)  # Note the quotes around 'BookRequest'
        created_date = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = ('user', 'book_request')

        def __str__(self):
            return f"{self.user.username} likes {self.book_request.title}"