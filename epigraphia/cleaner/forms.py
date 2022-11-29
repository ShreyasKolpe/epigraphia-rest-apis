from django import forms


class CleanerForm(forms.Form):
    input_str = forms.CharField(widget=forms.Textarea, label='Paste here the text to be cleaned')
    lang = forms.ChoiceField(choices=[('kn', 'Kannada')], label='Choose language of the script')
    process_e = forms.BooleanField(label='Choose whether to find and substitute ē', required=False)
    process_o = forms.BooleanField(label='Choose whether to find and substitute ō', required=False)
    process_s = forms.BooleanField(label='Choose whether to find and substitute the common sequence śrī', required=False)
    process_n = forms.BooleanField(label='Choose whether to smartly process anunasika-consonant clusters', required=False)
