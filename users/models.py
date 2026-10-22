import random
from django.contrib.auth.models import User
from django.db import models


class UserConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6, verbose_name="Код подтверждения")

    def __str__(self):
        return f"Код для {self.user.username}: {self.code}"

    @staticmethod
    def generate_code():

        return str(random.randint(100000, 999999))