from django.db import models

# Create your models here.

class Diabitic(models.Model):
    Patient_ID = models.AutoField(primary_key=True,auto_created=True,editable=False, serialize=True)
    Age = models.IntegerField()
    Gender = models.IntegerField()
    Blood_Pressure = models.IntegerField()
    Pregnancies = models.IntegerField()
    SkinThickness = models.CharField(max_length=5)
    Insulin=models.CharField(max_length=5)
    Glucose =models.CharField(max_length=5)
    BMI=models.CharField(max_length=5)
    Age=models.CharField(max_length=5)
    Result =models.CharField(max_length=1)

    def __str__(self):
        return self.Patient_ID
