from django.db import models

class Menu_ithems(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    roditel = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name  = 'dochernii')
    menu_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    