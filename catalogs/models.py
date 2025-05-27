from django.db import models

class Catalog(models.Model):
  name  = models.CharField(max_length=255)
  title = models.TextField(blank=True, null=True)
  
  def __str__(self):
    return f"{self.name} {self.title}"
  
  

