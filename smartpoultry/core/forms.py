from django import forms
from production.models import MortalityRecord, ProductionRecord


class StyledModelForm(forms.ModelForm):
    """Apply Bootstrap styling to generated form fields."""
    date_input_fields = {'date'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class
            if name in self.date_input_fields:
                field.widget = forms.DateInput(
                    attrs={'class': 'form-control', 'type': 'date'},
                    format='%Y-%m-%d',
                )


class ProductionRecordForm(StyledModelForm):
    class Meta:
        model = ProductionRecord
        fields = ['flock', 'product_type', 'quantity', 'unit', 'date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MortalityRecordForm(StyledModelForm):
    class Meta:
        model = MortalityRecord
        fields = ['flock', 'quantity', 'reason', 'date', 'description', 'notes']
        labels = {
            'flock': 'Flock ID to reduce',
        }
        help_texts = {
            'flock': 'Choose the flock whose quantity will be reduced by this mortality record.',
            'quantity': 'This number will be subtracted from the selected flock.',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
