from django.db import models


class Helligdag(models.Model):
    dag = models.DateField(
        unique=True,
    )

    def __str__(self):
        return str(self.dag)

    class Meta:
        verbose_name_plural = "Helligdage"
