# REST APIs for Epigraphia Carnatica database

This repo will contain code for the REST APIs to access the database containing 'cleaned' inscriptions from Epigraphia Carnatica (EC). See ['Cleaning' Epigraphia Carnatica for Knowledge Graphs](https://github.com/ShreyasKolpe/epigraphia-data-cleaning) for details on the (currently manual) process of obtaining cleaned information from EC.

The database is being built privately and step-by-step. Once the backend and frontend are in place, the database is planned to be hosted online. Building on this, the database is intended to feed into a project to build knowledge graphs from the inscriptions in EC. This is planned as a prototype.

## ER Schema

The following ER schema has been developed:![er_schema](https://user-images.githubusercontent.com/13967444/163443220-3d36cb1a-63f4-43e0-9938-d8afbe544c8f.svg)

EC is a series of volumes (here called **source_text**). Each volume has chapter-like geographical subdivisions (here called **source_text_chapter**). The atomic 'object' is the inscription itself (called **inscription**), whose information is spread across the book under different headings, but using a single numbering for the geographical subdivision. Primarily, this is three-fold: the inscription text in Indic script, inscription text in 'Roman' (Latin) characters, and translation in English. At this stage, the project only involves itself with the latter two (called **transliteration** and **translation** respectively).

## Backend

The backend will be developed in Python using the Django framework.

## REST APIs

Register APIs are meant to be create or update i.e., upsert.


Get APIs are read-only. (Here, the semantics of get is that of fetching, and not that of HTTP GET method. Thus, get is sometimes performed using POST as well)

### Source Text

1. **Register the text**

Note: Need to implement upsert, not just insert

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
	"publication_year": "1978"
}
```

Note: `title` is the only mandatory field, other fields can be blank

Response:

```
{
    "message": "Source text registered successfully",
    "data": {
        "source_text_id": ,
        "source_text_series": "",
        "source_text_volume": "",
        "source_text_title": ""
    }
}
```

2. **Get all registered texts**

Request:

```
GET /api/v1/source_text
```

Response:

```
{
    "source_texts": [ ,
        ,
        ...
    ]
}
```


### Source Text Chapter

1. **Register the chapter**

Note: Need to implement upsert, not just insert

Request:

```
POST /api/v1/source_text_chapter

{
	"chapter_title": "",
	"source_text": {
		"title": "",
        "subtitle": "",
        "series": "",
		"volume": ""
	}
}
```

Note: `chapter_title` is the only mandatory field, and any combination of attributes of `source_text` can be supplied to identify it accurately 

Response:

```
{
    "message": "Chapter registered successfully",
    "data": {
        "source_text_chapter_id": ,
        "source_text_chapter_title": "",
        "source_text": {
            "source_text_id": ,
            "source_text_series": "",
            "source_text_volume": "",
            "source_text_title": ""
        }
    }
}
```

2. **Get all registered chapters given text**


Request:

```
POST /api/v1/source_text_chapter/search

{
	"title": "",
    "subtitle": "",
    "series": "",
	"volume": ""
}
```

Note: Any combination of attributes of `source_text` can be supplied to identify it

Response:

```
{
    "message": "Successfully found these records",
    "data": [
        {
            "chapter_title": "",
            "source_text_title": ""
        },
        ...
    ]
}
```

### Inscription

1. **Register transliteration and/or translation for inscription**
2. **Get complete inscription object by text, chapter and inscription number** (using the view)