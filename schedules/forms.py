from genericpath import exists
from django import forms



class DoctorScheduleForm(forms.Form):
    date = forms.DateField(required=True)
    start_time = forms.TimeField(required=True)
    end_time = forms.TimeField(required=True)
    doctor = forms.ChoiceField(required=True, )
    clinic = forms.ChoiceField(required=True,)

    def clean_end_time(self):
        end_time1 = self.cleaned_data['end_time']
        start_time1 = self.cleaned_data['start_time']
        if end_time1<start_time1:
            raise forms.ValidationError("End Date must be later than start time")
        return end_time1


class ScheduleUploadForm(forms.Form):
    sheet = forms.FileField()