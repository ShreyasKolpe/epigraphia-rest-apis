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


Get APIs are read-only.

### Source Text

1. **Register the text**
2. **Get all registered texts**

### Source Text Chapter

1. **Register the chapter**
2. **Get all registered chapters given text**

### Inscription

1. **Get all inscriptions in text and chapter**
2. **Register transliteration for inscription**
3. **Register translation for inscription**
4. **Get complete inscription object by text, chapter and inscription number**