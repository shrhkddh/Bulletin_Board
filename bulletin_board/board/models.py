from django.db import models

class Board(models.Model):
    name        = models.CharField(max_length = 100)
    password    = models.CharField(max_length = 500)
    title       = models.CharField(max_length = 200)
    description = models.CharField(max_length = 5000)
    user_ip     = models.CharField(max_length = 500)
    updated_at  = models.DateField(auto_now = True)

    class Meta:
        db_table = 'boards'