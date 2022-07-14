from django import forms
from .models import Vehicle, Driver


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_name'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['capacity'].widget.attrs.update({"class": "form-control"})
        self.fields['company'].widget.attrs.update({"class": "form-control"})


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'national_id', 'mobile_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['national_id'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['mobile_number'].widget.attrs.update(
            {"class": "form-control"})
