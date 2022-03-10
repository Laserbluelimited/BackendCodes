from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class ScheduleDates(models.Model):
    id = models.IntegerField('appointment_date_id', primary_key=True, unique=True)
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    duration = models.DurationField('duration')
    clinic = models.ForeignKey('clinic_mgt.Clinic',unique=False, on_delete=models.CASCADE, default=1130000)
    doctor = models.ForeignKey( 'clinic_mgt.Doctor',unique=False, on_delete=models.CASCADE, default=1170000,)
    date = models.DateField('date')
    day_of_week = models.CharField('day_of_week', max_length=10, null=True)
    s_time = models.TimeField('actual_star_time')
    e_time = models.TimeField('actual_end_time')

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

    def get_duration(self):
        return self.duration/60000000

    def get_start_moment(self):
        return self.start_time.isoformat()

    def get_end_moment(self):
        return self.end_time.isoformat()
    
    def __str__(self):
        return "Appointment start time: " +self.start_time

    def save(self, *args, **kwargs):
        if not self.duration:
            self.duration = self.end_time - self.start_time
        if self.start_time.date() == self.end_time.date():
            self.date = self.end_time.date()
            self.day_of_week = self.end_time.strftime('%A')
        if not self.s_time:
            self.s_time = self.start_time.time()
        if not self.e_time:
            self.e_time = self.end_time.time()
        return super(ScheduleDates,self).save(*args, **kwargs)
        
