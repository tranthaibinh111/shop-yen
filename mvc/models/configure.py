from django.db import models


class Configure(models.Model):
    # SendGrid send 100 emails every date
    send_email = models.IntegerField(default=100)
    unit_money = models.CharField(max_length=10, default="VND")
    unit_weight = models.CharField(max_length=5, default="kg")

    def __str__(self):
        return "Configure APP"
