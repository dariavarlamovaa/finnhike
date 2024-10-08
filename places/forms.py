from django import forms

from places.models import Place


class PlaceSelectorForm(forms.Form):
    months = [
        ('january', 'January'), ('february', 'February'), ('march', 'March'),
        ('april', 'April'), ('may', 'May'), ('june', 'June'),
        ('july', 'July'), ('august', 'August'), ('september', 'September'),
        ('october', 'October'), ('november', 'November'), ('december', 'December')
    ]
    city = forms.ChoiceField(choices=[(city, city) for city in
                                      Place.objects.values_list('city', flat=True).order_by('city').distinct()],
                             required=False)
    month = forms.ChoiceField(choices=months, required=False)
