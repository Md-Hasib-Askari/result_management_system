from django import forms

SECTION_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
)
class StudentSearchForm(forms.Form):
    roll = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'border-2 border-gray-300 bg-white h-10 px-5 pr-16 rounded-lg text-sm focus:outline-none'}))
    section = forms.ChoiceField(choices=SECTION_CHOICES,required=False, widget=forms.Select(attrs={'class': 'form-control'}))
