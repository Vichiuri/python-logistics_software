from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_name'].widget.attrs.update({"class": "form-control"})
        self.fields['capacity'].widget.attrs.update({"class": "form-control"})
