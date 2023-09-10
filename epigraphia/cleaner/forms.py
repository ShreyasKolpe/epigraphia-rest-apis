from django import forms


class CleanerForm(forms.Form):
    input_str = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 100}),
                                label='Paste here the text to be cleaned')
    lang = forms.ChoiceField(choices=[('kn', 'Kannada')], label='Choose language of the script')
    process_a = forms.BooleanField(label='Choose whether to find and substitute ā', required=False, initial=True)
    process_e = forms.BooleanField(label='Choose whether to find and substitute ē', required=False, initial=True)
    process_o = forms.BooleanField(label='Choose whether to find and substitute ō', required=False, initial=True)
    process_u = forms.BooleanField(label='Choose whether to find and substitute ū', required=False, initial=True)
    process_s = forms.BooleanField(label='Choose whether to find and substitute ś and Ś', required=False, initial=True)
    process_n = forms.BooleanField(label='Choose whether to smartly process anunāsika-consonant clusters',
                                   required=False, initial=True)
    process_jn = forms.BooleanField(label='Choose whether to find and substitute (probable) ñ',
                                    required=False, initial=True)
    process_m = forms.BooleanField(label='Choose whether to find and substitute (probable) ṁ',
                                   required=False, initial=True)
    process_sri = forms.BooleanField(label='Choose whether to find and substitute the common sequence śrī',
                                     required=False, initial=True)

