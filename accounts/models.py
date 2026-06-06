from django.db import models

class UserProfile(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


    email = models.EmailField(
        unique=True
    )

  

  
    country = models.CharField(
        max_length=50
    )

    
    password = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profiles/')
    def __str__(self):
        return self.user.username