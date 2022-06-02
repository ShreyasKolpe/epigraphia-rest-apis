from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from apis import views, models
import json

# Create your views here.


def home(request):

    inscription_json = views.SourceTextView().get(request).content
    context = {
        'source_texts': json.loads(inscription_json.decode('utf-8'))
    }

    return render(request, 'index.html', context)


def inscription(request, inscription_id):

    inscription_json = views.InscriptionJoinedView().get(request, inscription_id).content
    inscription = json.loads(inscription_json.decode('utf-8'))['data']
    chapter_id = inscription['chapter']['id']
    other_inscriptions_in_chapter = models.Inscription.objects\
        .filter(source_text_chapter__source_text_chapter_id=chapter_id).order_by('source_text_inscription_number')
    other_inscriptions_in_chapter = list(other_inscriptions_in_chapter)
    other_inscriptions = [
        {
            "inscription_id": other_inscription.inscription_id,
            "inscription_number": other_inscription.source_text_inscription_number
        } for other_inscription in other_inscriptions_in_chapter
    ]
    context = {
        'other_inscriptions': other_inscriptions,
        'inscription': inscription
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
