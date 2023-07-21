from django import forms


class CleanerForm(forms.Form):
    input_str = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 100}),
                                label='Paste here the text to be cleaned')
    lang = forms.ChoiceField(choices=[('kn', 'Kannada')], label='Choose language of the script')
    process_a = forms.BooleanField(label='Choose whether to find and substitute ā', required=False)
    process_e = forms.BooleanField(label='Choose whether to find and substitute ē', required=False)
    process_o = forms.BooleanField(label='Choose whether to find and substitute ō', required=False)
    process_s = forms.BooleanField(label='Choose whether to find and substitute ś and Ś', required=False)
    process_n = forms.BooleanField(label='Choose whether to smartly process anunasika-consonant clusters', required=False)
    process_jn = forms.BooleanField(label='Choose whether to find and substitute (probable) ñ', required=False)
    process_m = forms.BooleanField(label='Choose whether to find and substitute (probable) ṁ', required=False)
    process_sri = forms.BooleanField(label='Choose whether to find and substitute the common sequence śrī',
                                     required=False)

