from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='split')
@stringfilter
def split(value, arg):
    return value.split(arg)


@register.inclusion_tag('fmt_inscription.html', takes_context=True)
def fmt_inscription(context):

    print([x for x in context['inscription']])
    inscription_components = {
        'translation_header': context['inscription']['translation_header'],
        'translation': context['inscription']['translation'],
        'translation_footnotes': context['inscription']['translation_footnotes']
    }

    tsltr_header_components = process_text(context['inscription']['transliteration_header'])
    inscription_components['inscription_text_header'] = tsltr_header_components['first_component']
    inscription_components['transliteration_header'] = tsltr_header_components['second_component']

    tsltr_components = process_text(context['inscription']['transliteration'])
    inscription_components['inscription_text'] = tsltr_components['first_component']
    inscription_components['transliteration'] = tsltr_components['second_component']

    tsltr_footnotes_components = process_text(context['inscription']['transliteration_footnotes'])
    inscription_components['inscription_text_footnotes'] = tsltr_footnotes_components['first_component']
    inscription_components['transliteration_footnotes'] = tsltr_footnotes_components['second_component']

    return inscription_components


def process_text(text):

    first_component = ''
    second_component = text

    if text.startswith('--indic_text--'):
        first_component = text.split('--end_indic_text--')[0].split('--indic_text--')[1]
        second_component = text.split('--end_indic_text--')[1]

    return {
        'first_component': first_component,
        'second_component': second_component
    }