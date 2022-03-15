from venv import create
from django.db import models

# Create your models here.

class Appointment(models.Model):
    id = models.IntegerField('appointment_id', primary_key=True)
    doctor = models.ForeignKey('clinic_mgt.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinic_mgt.Clinic', on_delete=models.CASCADE)
    start_time = models.DateTimeField('start_time', null=True)
    end_time = models.DateTimeField('end_time', null=True)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    date = models.DateField('date', null=True)
    day_of_week = models.CharField('day_of_week', max_length=10, null=True)
    s_time = models.TimeField('actual_star_time', null=True)
    e_time = models.TimeField('actual_end_time', null=True)
    notes = models.TextField('notes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.time) + ' ' + str(self.doctor)
    def get_start_time(self):
        return self.s_time

    def get_end_time(self):
        return self.e_time

    def get_day_of_week(self):
        return self.day_of_week

    def get_date(self):
        return self.date

    def get_doctor(self):
        return self.doctor

    def get_clinic(self):
        return self.clinic


    def get_start_moment(self):
        return self.start_time.isoformat()

    def get_end_moment(self):
        return self.end_time.isoformat()
    
    def __str__(self):
        return "Appointment start time: " +self.start_time

    def save(self, *args, **kwargs):
        if self.start_time.date() == self.end_time.date():
            self.date = self.end_time.date()
            self.day_of_week = self.end_time.strftime('%A')
        if not self.s_time:
            self.s_time = self.start_time.time()
        if not self.e_time:
            self.e_time = self.end_time.time()
        return super(Appointment,self).save(*args, **kwargs)
