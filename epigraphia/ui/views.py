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
    inscriptions_in_chapter_list = extract_inscription_id_and_number_attributes(inscriptions_in_chapter)

    location_id = inscription_from_json['location']['id']
    inscription_search_object = {
        "location": {
            "id": location_id
        }
    }
    inscriptions_at_location = views.search_inscriptions(inscription_search_object)
    inscriptions_at_location = list(inscriptions_at_location)
    inscriptions_at_location_list = extract_inscription_id_and_number_attributes(inscriptions_in_chapter)

    context = {
        'inscription': inscription_from_json,
        'inscriptions_in_chapter': inscriptions_in_chapter_list,
        'inscriptions_at_location': inscriptions_at_location_list
    }
    return render(request, 'inscription.html', context)


def inscription_search(request):

    if request.method == 'POST':
        inscription_search_object = {
            "chapter": {
                "id": request.POST.get("sourceTextChapter", 0)
            }
        }
        inscriptions_in_chapter = list(views.search_inscriptions(inscription_search_object))
        inscriptions_in_chapter_list = extract_inscription_id_and_number_attributes(inscriptions_in_chapter)
        first_inscription = sorted(inscriptions_in_chapter_list, key=lambda inscr: inscr["inscription_number"])[0]
        inscription_id = first_inscription["inscription_id"]
        return redirect(f"/inscription/{inscription_id}")
    else:
        return HttpResponseBadRequest("Invalid method")


def inscriptions_by_location(request, location_id):

    inscription_search_object = {
        "location": {
            "id": location_id
        }
    }
    inscriptions_at_location = list(views.search_inscriptions(inscription_search_object))
    inscriptions_at_location_list = extract_inscription_id_and_number_attributes(inscriptions_at_location)
    first_inscription = sorted(inscriptions_at_location_list, key=lambda inscr: inscr["inscription_number"])[0]
    inscription_id = first_inscription["inscription_id"]
    return redirect(f"/inscription/{inscription_id}")

def extract_inscription_id_and_number_attributes(inscriptions):

    inscriptions_with_id_and_number = [
        {
            "inscription_id": found_inscription.inscription_id,
            "inscription_number": found_inscription.source_text_inscription_number
        } for found_inscription in inscriptions
    ]
    return inscriptions_with_id_and_number
