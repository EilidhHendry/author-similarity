from django import forms

class InputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=False)
    input_file = forms.FileField(required=False)

    def clean(self):
        text = self.cleaned_data['text']
        input_file = self.cleaned_data['input_file']
        if not text and not input_file:
            raise forms.ValidationError('require text or file')
