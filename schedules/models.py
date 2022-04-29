from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime, date

# Create your models here.
class TimeSlots(models.Model):
    duration = models.DurationField('duration')
    schedule = models.ForeignKey('ScheduleDates', on_delete=models.CASCADE)
    start_time = models.TimeField('actual_star_time')
    end_time = models.TimeField('actual_end_time')
    status = models.CharField('status', max_length=10, choices=[(0, 'not booked'),(1, 'temporarily booked'), ('2', 'paid for')])

    def update_status(self, status):
        self.status = status
        self.save()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_day_of_week(self):
        return self.schedule.day_of_week

    def get_date(self):
        return self.schedule.date

    def get_doctor(self):
        return self.schedule.doctor

    def get_clinic(self):
        return self.schedule.clinic

    def get_duration(self):
        return self.duration/60000000

    

    def save(self, *args, **kwargs):
        if not self.duration:
            self.duration = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
        return super(TimeSlots,self).save(*args, **kwargs)
        




class ScheduleDates(models.Model):
    id = models.AutoField('sche_dates_id', primary_key=True)
    duration = models.DurationField('duration')
    clinic = models.ForeignKey('clinic_mgt.Clinic',unique=False, on_delete=models.CASCADE, )
    doctor = models.ForeignKey( 'clinic_mgt.Doctor',unique=False, on_delete=models.CASCADE,)
    date = models.DateField('date')
    day_of_week = models.CharField('day_of_week', max_length=10, null=True)
    start_time = models.TimeField('actual_star_time')
    end_time = models.TimeField('actual_end_time')
    slug = models.SlugField(max_length=255, help_text='Unique Value for product page URL, created from name.')


    

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

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

    

    def save(self, *args, **kwargs):
        if not self.duration:
            self.duration = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
        self.day_of_week = self.date.strftime('%A')
        if not self.slug:
            name = self.doctor.first_name + str(self.id)
            self.slug = slugify(name)
        return super(ScheduleDates,self).save(*args, **kwargs)
        
