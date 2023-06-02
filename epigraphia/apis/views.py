from django.http import JsonResponse
from django.views import View
from apis import models
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SourceTextView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        title = data.get('title', '')
        if not title:
            return badRequestError("The title cannot be blank")

        # Check if object exists, if so do an update. Else, create new object
        try:
            source_text = models.SourceText.objects.get(source_text_title__iexact=title)
        except models.SourceText.DoesNotExist:
            source_text = models.SourceText(source_text_title=title)

        # Set updatable attributed
        source_text.source_text_subtitle = data.get('subtitle', '')
        source_text.source_text_series = data.get('series', '')
        source_text.source_text_volume = data.get('volume', '')
        source_text.source_text_author = data.get('author', '')
        source_text.source_text_publisher = data.get('publisher', '')
        source_text.source_text_publication_place = data.get('publication_place', '')
        publication_year = data.get('publication_year', '')
        if not publication_year:
            publication_year = '0000'
        publication_ymd = "{}-01-01".format(publication_year)
        source_text.source_text_publication_date = datetime.strptime(publication_ymd, '%Y-%m-%d')

        # Insert into db
        source_text.save()

        # Format the response and return it
        data = self.extract_source_text_attributes(source_text)
        response = {
            "status": 200,
            "message": "Source text registered successfully",
            "data": data
        }
        return JsonResponse(response)

    def get(self, request, text_id=None):
        if text_id:

            # Get object by id. If it doesn't exist, return error
            try:
                source_text = models.SourceText.objects.get(source_text_id=text_id)
            except models.SourceText.DoesNotExist:
                return notFoundError(f"Source text with id {text_id} not found")

            # Format the response and return it
            data = self.extract_source_text_attributes(source_text)
            response = {
                "status": 200,
                "message": "Successfully found this record",
                "data": data
            }
            return JsonResponse(response)

        else:

            # Get all objects, format the response and return it
            all_source_texts = models.SourceText.objects.all()
            data = [{
                    "id": source_text.source_text_id,
                    "title": source_text.source_text_title,
                    "subtitle": source_text.source_text_subtitle,
                    "series": source_text.source_text_series,
                    "volume": source_text.source_text_volume,
                } for source_text in all_source_texts]
            response = {
                "status": 200,
                "message": "Successfully found these records",
                "data": data
            }
            return JsonResponse(response)

    def extract_source_text_attributes(self, source_text):
        # Helper method
        return {
            "id": source_text.source_text_id,
            "title": source_text.source_text_title,
            "subtitle": source_text.source_text_subtitle,
            "series": source_text.source_text_series,
            "volume": source_text.source_text_volume,
            "author": source_text.source_text_author,
            "publisher": source_text.source_text_publisher,
            "publication_place": source_text.source_text_publication_place,
            "publication_date": source_text.source_text_publication_date
        }


@method_decorator(csrf_exempt, name='dispatch')
class SourceTextChapterView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        chapter_title = data.get('chapter_title', '')
        if not chapter_title:
            return badRequestError("The chapter title cannot be blank")
        source_text = data.get('source_text', {})
        if not source_text:
            return badRequestError("Need source text information for registering")

        # Check if chapter already exists, if so then do an update. Else create new object
        try:
            source_text_chapter = models.SourceTextChapter.objects.get(source_text_chapter_title__iexact=chapter_title)
        except models.SourceTextChapter.DoesNotExist:
            source_text_chapter = models.SourceTextChapter(source_text_chapter_title=chapter_title)

        # Find the source text and set the updatable attributes
        id = source_text.get('id', None)
        title = source_text.get('title', '')
        subtitle = source_text.get('subtitle', '')
        series = source_text.get('series', '')
        volume = source_text.get('volume', '')

        # If id is supplied, the object can be found directly. Else, filter using the other attributes
        query_set = models.SourceText.objects
        if id:
            found_source_text = query_set.get(source_text_id=id)
        else:
            if title:
                query_set = query_set.filter(source_text_title__icontains=title)
            if series:
                query_set = query_set.filter(source_text_series__icontains=series)
            if volume:
                query_set = query_set.filter(source_text_volume__icontains=volume)
            if subtitle:
                query_set = query_set.filter(source_text_subtitle__icontains=subtitle)

            source_texts = list(query_set)
            if len(source_texts) == 0:
                return badRequestError("No matching source text found, reexamine the attributes")
            elif len(source_texts) > 1:
                return badRequestError("Found more than one matching source text, reexamine the attributes")

            found_source_text = source_texts[0]

        # Set the source_text for the chapter
        source_text_chapter.source_text = found_source_text
        source_text_chapter.save()

        # Format the response and return it
        response_data = extract_chapter_attributes(source_text_chapter)
        response = {
            "status": 200,
            "message": "Chapter registered successfully",
            "data": response_data
        }
        return JsonResponse(response)

    def get(self, request, chapter_id):

        try:
            source_text_chapter = models.SourceTextChapter.objects.get(source_text_chapter_id=chapter_id)
        except models.SourceTextChapter.DoesNotExist:
            return notFoundError(f"Source text chapter with id {chapter_id} not found")

        # Format the response and return it
        data = extract_chapter_attributes(source_text_chapter)
        response = {
            "status": 200,
            "message": "Successfully found this record",
            "data": data
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt)
def get_source_text_chapters_by_search(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        source_text = data.get('source_text', {})
        text_id = source_text.get('id', None)

        query_set = models.SourceTextChapter.objects
        if text_id:
            query_set = query_set.filter(source_text__source_text_id=text_id)
            # found_chapters = [found_chapter, ]
        else:
            title = source_text.get('title', '')
            subtitle = source_text.get('subtitle', '')
            series = source_text.get('series', '')
            volume = source_text.get('volume', '')
            if title:
                query_set = query_set.filter(source_text__source_text_title__icontains=title)
            if series:
                query_set = query_set.filter(source_text__source_text_series__icontains=series)
            if volume:
                query_set = query_set.filter(source_text__source_text_volume__icontains=volume)
            if subtitle:
                query_set = query_set.filter(source_text_source_text_subtitle__icontains=subtitle)

        found_chapters = list(query_set)

        response_data = []
        for chapter in found_chapters:
            response_data.append(extract_chapter_attributes(chapter))
        response = {
            "status":200,
            "message": "Successfully found these records",
            "data": response_data
        }
        return JsonResponse(response)

    else:
        return notAllowedError("Method not allowed")


def extract_chapter_attributes(source_text_chapter):
    # Helper method
    return {
        "chapter_id": source_text_chapter.source_text_chapter_id,
        "chapter_title": source_text_chapter.source_text_chapter_title,
        "source_text": {
            "id": source_text_chapter.source_text.source_text_id,
            "title": source_text_chapter.source_text.source_text_title,
            "subtitle": source_text_chapter.source_text.source_text_subtitle,
            "series": source_text_chapter.source_text.source_text_series,
            "volume": source_text_chapter.source_text.source_text_volume,
        }
    }


@method_decorator(csrf_exempt, name='dispatch')
class InscriptionView(View):
    def post(self, request):

        data = json.loads(request.body.decode('utf-8'))

        chapter = data.get('chapter', {})
        inscription_number = data.get('inscription_number', None)
        inscription_id = data.get('inscription_id', None)

        # If there is no inscription_id
        if not inscription_id:
            # and neither are there chapter and inscription_number,
            if not chapter or not inscription_number:
                return badRequestError("Need chapter information and inscription number for registration")
            # else, use chapter and inscription number
            else:
                # check if inscription exists already
                chapter_id = chapter.get('id', None)
                chapter_title = chapter.get('chapter_title', '')
                inscription_number = data.get('inscription_number', None)

                inscription_queryset = models.Inscription.objects
                if chapter_id:
                    inscription_queryset = inscription_queryset.filter(source_text_chapter__source_text_chapter_id=chapter_id)
                elif chapter_title:
                    inscription_queryset = inscription_queryset.filter(source_text_chapter__source_text_chapter_title=chapter_title)
                if inscription_number:
                    inscription_queryset = inscription_queryset.filter(source_text_inscription_number=inscription_number)

                inscriptions = list(inscription_queryset)
                # If found, use it. Else, create a new object and set its chapter and inscription number
                if inscription_queryset:
                    inscription = inscriptions[0]

                else:
                    # Create new inscription object
                    inscription = models.Inscription()

                    # Set its inscription number
                    inscription.source_text_inscription_number = inscription_number

                    # Set its chapter
                    chapter_queryset = models.SourceTextChapter.objects
                    if chapter_id:
                        chapter = chapter_queryset.get(source_text_chapter_id=chapter_id)
                    elif chapter_title:
                        chapter_queryset = chapter_queryset.get(source_text_chapter_title__icontains=chapter_title)

                        chapters = list(chapter_queryset)
                        if not chapters:
                            return badRequestError("Matching chapter not found")
                        if len(chapters) > 1:
                            return badRequestError("Matches more than one chapter")
                        chapter = chapters[0]

                    inscription.source_text_chapter = chapter

        else:
            # If inscription_id is supplied, use it to find object directly. If not found, return error
            try:
                inscription = models.Inscription.objects.get(inscription_id=inscription_id)
            except models.Inscription.DoesNotExist:
                return notFoundError(f"Inscription with id {inscription_id} does not exist")

            # It is possible to set the chapter and inscription_number since that information is not being used to id
            inscription.source_text_inscription_number = inscription_number

            if chapter:
                chapter_id = chapter.get('id', None)
                chapter_title = chapter.get('chapter_title', '')

                chapter_queryset = models.SourceTextChapter.objects
                if chapter_id:
                    chapter = chapter_queryset.get(source_text_chapter_id=chapter_id)
                elif chapter_title:
                    chapter_queryset = chapter_queryset.get(source_text_chapter_title__icontains=chapter_title)

                    chapters = list(chapter_queryset)
                    if not chapters:
                        return badRequestError("Matching chapter not found")
                    if len(chapters) > 1:
                        return badRequestError("Matches more than one chapter")
                    chapter = chapters[0]

                inscription.source_text_chapter = chapter

        # Insert into db
        inscription.save()

        # Check if translation exists for this inscription. If so update, otherwise insert
        try:
            translation = models.Translation.objects.get(inscription__inscription_id=inscription.inscription_id)
        except models.Translation.DoesNotExist:
            translation = models.Translation()
            translation.inscription=inscription
        translation.header = data.get('translation_header', '')
        translation.translation = data.get('translation', '')
        translation.footnotes = data.get('translation_footer', '')

        translation.save()

        # Check if transliteration exists for this inscription. If so update, otherwise insert
        try:
            transliteration = models.Transliteration.objects.get(inscription__inscription_id=inscription.inscription_id)
        except models.Transliteration.DoesNotExist:
            transliteration = models.Transliteration()
            transliteration.inscription=inscription
        transliteration.header = data.get('transliteration_header', '')
        transliteration.transliteration = data.get('transliteration', '')
        transliteration.footnotes = data.get('transliteration_footer', '')

        transliteration.save()

        # Format the response and return it
        response_data = {
                "source_text": {
                    "id": inscription.source_text_chapter.source_text.source_text_id,
                    "title": inscription.source_text_chapter.source_text.source_text_title,
                    "subtitle": inscription.source_text_chapter.source_text.source_text_subtitle,
                    "series": inscription.source_text_chapter.source_text.source_text_series,
                    "volume": inscription.source_text_chapter.source_text.source_text_volume,
                    "author": inscription.source_text_chapter.source_text.source_text_author,
                    "publisher": inscription.source_text_chapter.source_text.source_text_publisher,
                    "publication_place": inscription.source_text_chapter.source_text.source_text_publication_place,
                    "publication_date": inscription.source_text_chapter.source_text.source_text_publication_date
                },
                "chapter": {
                    "id": inscription.source_text_chapter.source_text_chapter_id,
                    "title": inscription.source_text_chapter.source_text_chapter_title,
                },
                "inscription_id": inscription.inscription_id,
                "inscription_number": inscription.source_text_inscription_number,
                "translation_header": translation.header,
                "translation": translation.translation,
                "translation_footer": translation.footnotes,
                "transliteration_header": transliteration.header,
                "transliteration": transliteration.transliteration,
                "transliteration_footer": transliteration.footnotes
        }
        response = {
            "status": 200,
            "message": "Successfully registered translation and/or transliteration",
            "data": response_data
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class InscriptionJoinedView(View):
    def get(self, request, inscription_id=None):

        try:
            inscription = models.InscriptionJoined.objects.get(inscription_id=inscription_id)
        except models.InscriptionJoined.DoesNotExist:
            return notFoundError(f"Inscription with id {inscription_id} not found")

        data = extract_inscription_attributes(inscription)
        response = {
            "status": 200,
            "message": "Successfully found this record",
            "data": data
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt)
def get_inscriptions_by_search(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        inscriptions = search_inscriptions(data)
        response_data = []
        for inscription in inscriptions:
            response_data.append(extract_inscription_attributes(inscription))
        response = {
            "status": 200,
            "message": "Successfully found these records",
            "data": response_data
        }
        return JsonResponse(response)

    else:
        return notAllowedError("Method not allowed")


def search_inscriptions(data):
    source_text = data.get('source_text', {})
    chapter = data.get('chapter', '')
    inscription_number = data.get('inscription_number', None)

    # Just chain filters according to the attributes given
    if not source_text and not chapter and not inscription_number:
        inscription_queryset = models.InscriptionJoined.objects.all()
    else:
        inscription_queryset = models.InscriptionJoined.objects
    if source_text:
        source_text_id = source_text.get('id', None)
        if source_text_id:
            inscription_queryset = inscription_queryset.filter(source_text_id=source_text_id)
        else:
            title = source_text.get('title', '')
            subtitle = source_text.get('subtitle', '')
            series = source_text.get('series', '')
            volume = source_text.get('volume', '')
            if title:
                inscription_queryset = inscription_queryset.filter(source_text_title__icontains=title)
            if series:
                inscription_queryset = inscription_queryset.filter(source_text_series__icontains=series)
            if volume:
                inscription_queryset = inscription_queryset.filter(source_text_volume__icontains=volume)
            if subtitle:
                inscription_queryset = inscription_queryset.filter(ource_text_subtitle__icontains=subtitle)

    if chapter:
        source_text_chapter_id = chapter.get('id', None)
        if source_text_chapter_id:
            inscription_queryset = inscription_queryset.filter(source_text_chapter_id=source_text_chapter_id)
        else:
            title = chapter.get('title', '')
            if title:
                inscription_queryset = inscription_queryset.filter(
                    source_text_chapter_title__icontains=source_text_chapter_id)

    if inscription_number:
        inscription_queryset = inscription_queryset.filter(source_text_inscription_number=inscription_number)

    return list(inscription_queryset)


def extract_inscription_attributes(inscription):
    # Helper method
    return {
        "source_text": {
            "id": inscription.source_text_id,
            "title": inscription.source_text_title,
            "subtitle": inscription.source_text_subtitle,
            "series": inscription.source_text_series,
            "volume": inscription.source_text_volume,
            "author": inscription.source_text_author,
            "publisher": inscription.source_text_publisher,
            "publication_place": inscription.source_text_publication_place,
            "publication_date": inscription.source_text_publication_date
        },
        "chapter": {
            "id": inscription.source_text_chapter_id,
            "title": inscription.source_text_chapter_title,
        },
        "inscription_id": inscription.inscription_id,
        "location": {
            "name": inscription.location_name,
            "coordinates": [inscription.coordinates[1], inscription.coordinates[0]] if inscription.coordinates else None
        },
        "inscription_number": inscription.source_text_inscription_number,
        "translation_header": inscription.translation_header,
        "translation": inscription.translation,
        "translation_footer": inscription.translation_footnotes,
        "transliteration_header": inscription.transliteration_header,
        "transliteration": inscription.transliteration,
        "transliteration_footer": inscription.transliteration_footnotes
    }


def notAllowedError(message):
    return JsonResponse({
        "status": 403,
        "message": message
    }, status=403)


def notFoundError(message):
    return JsonResponse({
        "status": 404,
        "message": message
    }, status=404)


def badRequestError(message):
    return JsonResponse({
        "status": 400,
        "message": message
    }, status=400)
