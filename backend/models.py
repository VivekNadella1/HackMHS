from django.db import models
from django.contrib.auth.models import User

class CollegeStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    sat = models.IntegerField(default=1400)
    act = models.IntegerField(null=True, blank=True, default=20)  
    race = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    income = models.CharField(max_length=1000)
    def get_user():
        return User.username
    
class ExtracurricularActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)
    ranking = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Extracurricular Activity: {self.activity_name}"
from django.db import models
from django.contrib.auth.models import User

class Award(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    award_name = models.CharField(max_length=255)
    award_type = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.award_name} ({self.user.username})"

class APCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.course} - {self.score}"