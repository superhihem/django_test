import os
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser

class Author(AbstractUser):
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.username} ({self.phone})"


class Trade(models.Model):
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    status = models.IntegerChoices("TradeStatus", "OPEN CLOSED")

    def __str__(self):
        return f"{self.title} | {self.author}"

def author_directory_path(instance, filename):
    # MEDIA_ROOT/<username>/<filename>_<10 rand chars>.<extention>
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    rand_str = ''.join(random.choice(chars) for _ in range(10))
    name, ext = os.path.splitext(filename)

    return f"user_content/{instance.author.username}/{name}_{rand_str}{ext}"

class TradeImage(models.Model):
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    image = models.FileField(upload_to=author_directory_path)

    def __str__(self):
        return f"{self.image.name} | {self.trade}"
