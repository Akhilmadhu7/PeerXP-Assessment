from django.db import models
from Assessment.settings import AUTH_USER_MODEL

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    created_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
