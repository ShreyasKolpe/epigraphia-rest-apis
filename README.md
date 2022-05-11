# REST APIs for Epigraphia Carnatica database

This repo will contain code for the REST APIs to access the database containing 'cleaned' inscriptions from Epigraphia Carnatica (EC). See ['Cleaning' Epigraphia Carnatica for Knowledge Graphs](https://github.com/ShreyasKolpe/epigraphia-data-cleaning) for details on the (currently manual) process of obtaining cleaned information from EC.

The database is being built privately and step-by-step. Once the backend and frontend are in place, the database is planned to be hosted online. Building on this, the database is intended to feed into a project to build knowledge graphs from the inscriptions in EC. This is planned as a prototype.

## ER Schema

The following ER schema has been developed:![er_schema](https://user-images.githubusercontent.com/13967444/163443220-3d36cb1a-63f4-43e0-9938-d8afbe544c8f.svg)

EC is a series of volumes (here called **source_text**). Each volume has chapter-like geographical subdivisions (here called **source_text_chapter**). The atomic 'object' is the inscription itself (called **inscription**), whose information is spread across the book under different headings, but using a single numbering for the geographical subdivision. Primarily, this is three-fold: the inscription text in Indic script, inscription text in 'Roman' (Latin) characters, and translation in English. At this stage, the project only involves itself with the latter two (called **transliteration** and **translation** respectively).

## Backend

The backend will be developed in Python using the Django framework.

Some thoughts:
1. Django is chosen as it enables rapid development. Python was a requirement keeping in mind extensibility to knowledge graphs, AI and NLP through Python support in such software.
2. Resources to learn Django:
    a. [Programming with Harry](https://www.youtube.com/playlist?list=PLK8cqdr55Tsv-D2HMdrnD32oOVBNvmxjr)
    b. Django [documentation](https://docs.djangoproject.com/en/4.0/), especially about models, fields and querying.
    c. Developing REST applications in [plain Django](https://stackabuse.com/creating-a-rest-api-in-python-with-django/) or with [Django REST Framework](https://stackabuse.com/creating-a-rest-api-with-django-rest-framework/). Both tutorials are brilliant and lay out the costs of choosing either approach. In this project, plain Django is used.
3. The Django admin portal provides CRUD operations on database through a UI and obliviates a good deal of rationale for generating own data entry portal involving Auth. Further customization through this [tutorial](https://realpython.com/customize-django-admin-python/). 
4. Free small-scale hosting of Python based applications including web apps at [Python Anywhere](https://www.pythonanywhere.com/).


## REST APIs

Register APIs are meant to be create or update i.e., upsert.


Get APIs are read-only. (Here, the semantics of get is that of fetching, and not that of HTTP GET method. Thus, get is sometimes performed using POST as well)

### Source Text

1. **Register the text**

Request:

```
POST /api/v1/source_text

{
	"title": "",
    "subtitle": "",
    "series": "",
    "volume": "",
	"author": "",
    "publisher": "",
    "publication_place": "",
	"publication_year": ""
}
```

**Note**: `title` is the only mandatory field, other fields can be blank

Response:

```
{
    "message": "Source text registered successfully",
    "data": {
        "id": ,
        "title": "",
        "subtitle": "",
        "series": "",
        "volume": "",
        "author": "",
        "publisher": "",
        "publication_place": "",
        "publication_year": ""
    }
}
```

2. **Get source text by id**

Request:

```
GET /api/v1/source_text/<id>
```

Response:

```
{
    "source_text": {
        "id": ,
        "title": "",
        "series": "",
        "volume": "",
        "author": "",
        "publisher": "",
        "publication_place": "",
        "publication_year": ""
    }
}
```

3. **Get all registered texts**

Request:

```
GET /api/v1/source_text
```

Response:

```
{
    "source_texts": [ 
        {
            "id": ,
            "title": "",
            "subtitle": "",
            "series": "",
            "volume": "",
        },
        ...
    ]
}
```


### Source Text Chapter

1. **Register the chapter**

Request:

```
POST /api/v1/source_text_chapter

{
	"chapter_title": "",
	"source_text": {
        "id": ,
		"title": "",
        "subtitle": "",
        "series": "",
		"volume": ""
	}
}
```

**Note**: `chapter_title` is a mandatory field. To identify `source_text` provide either the `id` or a combination of the other attributes. 

Response:

```
{
    "message": "Chapter registered successfully",
    "data": {
        "chapter_id": ,
        "chapter_title": "",
        "source_text": {
            "id": ,
            "title": "",
            "subtitle": "",
            "series": "",
            "volume": "",
        }
    }
}
```

2. **Get chapter by id**

Request:

```
GET /api/v1/source_text_chapter/<id>
```

Response:

```
{
    "chapter_id": ,
    "chapter_title": "",
    "source_text": {
        "id": ,
        "title": "",
        "subtitle": "",
        "series": "",
        "volume": "",
    }
}
```

3. **Get all registered chapters for a source text**


Request:

```
POST /api/v1/source_text_chapter/search

{
    "source_text": {
        "id": ,
        "title": "",
        "subtitle": "",
        "series": "",
        "volume": ""
    }
}
```

**Note**:  To identify `source_text` provide either the `id` or a combination of the other attributes. 

Response:

```
{
    "message": "Successfully found these records",
    "data": [
        {
            "chapter_id": "",
            "chapter_title": "",
            "source_text": {
                "id": ,
                "title": "",
                "subtitle": "",
                "series": "",
                "volume": ""
            }
        },
        ...
    ]
}
```

### Inscription

1. **Register transliteration and/or translation for inscription**

Request:

```
POST /api/v1/inscription

{
    "chapter": {
        "id": ,
        "title": ""
    },
    "inscription_id": ,
    "inscription_number": "",
    "translation_header": "",
    "translation": "",
    "translation_footer": "",
    "transliteration_header": "",
    "transliteration": "",
    "transliteration_footer": ""
}
```

**Note**: Provide either `id` or `title` to identify chapter. `inscription_number` cannot be null. `inscription_id` is provided for programmatic upsert and is not mandatory. The backend will first check if record exists, and then update the translation and transliteration attributes. Else, it will insert into the database and create the foreign key relations.

Response:

```
{
    "message": "Successfully registered translation and/or transliteration",
    "data": {
        "source_text": {
            "id": ,
            "title": "",
            "subtitle": "",
            "series": "",
            "volume": ""
        },
        "chapter": {
            "id": ,
            "title": "",
        }
        "inscription_id": ,
        "inscription_number": "",
        "translation_header": "",
        "translation": "",
        "translation_footer": "",
        "transliteration_header": "",
        "transliteration": "",
        "transliteration_footer": ""
    }
}
```

2. **Get complete inscription object by text, chapter and inscription number** (using the view)

Request:

```
POST /api/v1/inscription/search

{
    "source_text": {
        "id": ,
        "title": "",
        "subtitle": "",
        "series": "",
        "volume": "",
    },
    "chapter": {
        "id": ,
        "chapter_title": "",
    }
    "inscription_number": "",
}
```

**Note**: To identify `source_text` provide either the `id` or a combination of the other attributes. Some such information is mandatory. `chapter_title` and `inscription_number` are mandatory.

Response:

```

```