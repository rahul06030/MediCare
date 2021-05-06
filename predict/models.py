from django.db import models


class PredResults(models.Model):
    Patient_ID = models.AutoField(primary_key=True,auto_created=True, editable=False, serialize=True)
    Patient_Age = models.IntegerField()
    Patient_Gender = models.IntegerField()
    Patient_Blood_Pressure = models.IntegerField()
    Patient_Heartrate = models.IntegerField()
    Heart_Disease = models.CharField(max_length=30)

    def __str__(self):
        return self.Patient_ID
