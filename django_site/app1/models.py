import os
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

class Author(AbstractUser):
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.username} ({self.id})"


class Trade(models.Model):
    class TradeStatus(models.TextChoices):
        OPEN = "open", "Открыто"
        CLOSED = "closed", "Закрыто"

    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    status = models.CharField(choices=TradeStatus.choices, max_length=20, default=TradeStatus.OPEN)

    def get_images(self):
        return TradeImage.objects.filter(author=self.author.id)

    def __str__(self):
        return f"{self.title} ({self.id}) | {self.author}"

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

@receiver(models.signals.post_delete, sender=TradeImage)
def trade_image_file_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)