from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from apis import views, models
import json

# Create your views here.


def home(request):

    inscription_json = views.SourceTextView().get(request).content
    locations_json = views.LocationView().get(request).content
    context = {
        'source_texts': json.loads(inscription_json.decode('utf-8')),
        'all_locations': json.loads(locations_json.decode('utf-8'))
    }

    return render(request, 'index.html', context)


def inscription(request, inscription_id):

    inscription_json = views.InscriptionJoinedView().get(request, inscription_id).content
    inscription_from_json = json.loads(inscription_json.decode('utf-8'))['data']

    chapter_id = inscription_from_json['chapter']['id']
    inscription_search_object = {
        "chapter": {
            "id": chapter_id
        }
    }
    inscriptions_in_chapter = views.search_inscriptions(inscription_search_object)
    inscriptions_in_chapter = list(inscriptions_in_chapter)
    inscriptions_in_chapter_list = [
        {
            "inscription_id": other_inscription.inscription_id,
            "inscription_number": other_inscription.source_text_inscription_number
        } for other_inscription in inscriptions_in_chapter
    ]

    location_id = inscription_from_json['location']['id']
    inscription_search_object = {
        "location": {
            "id": location_id
        }
    }
    inscriptions_at_location = views.search_inscriptions(inscription_search_object)
    inscriptions_at_location = list(inscriptions_at_location)
    inscriptions_at_location_list = [
        {
            "inscription_id": other_inscription.inscription_id,
            "inscription_number": other_inscription.source_text_inscription_number
        } for other_inscription in inscriptions_at_location
    ]

    context = {
        'inscription': inscription_from_json,
        'inscriptions_in_chapter': inscriptions_in_chapter_list,
        'inscriptions_at_location': inscriptions_at_location_list
    }
    return render(request, 'inscription.html', context)


def inscription_search(request):
    if request.method == 'POST':
        chapter_id = request.POST.get("sourceTextChapter", 0)
        first_inscription = models.Inscription.objects \
            .filter(source_text_chapter__source_text_chapter_id=chapter_id).order_by('source_text_inscription_number')[:1].get()
        inscription_id = first_inscription.inscription_id
        return redirect(f"/inscription/{inscription_id}")
    else:
        return HttpResponseBadRequest("Invalid method")
