# REST APIs for Epigraphia Carnatica database

This repo will contain code for the REST APIs to access the database containing 'cleaned' inscriptions from Epigraphia Carnatica (EC). See ['Cleaning' Epigraphia Carnatica for Knowledge Graphs](https://github.com/ShreyasKolpe/epigraphia-data-cleaning) for details on the (currently manual) process of obtaining cleaned information from EC.

The database is being built privately and step-by-step. Once the backend and frontend are in place, the database is planned to be hosted online. Building on this, the database is intended to feed into a project to build knowledge graphs from the inscriptions in EC. This is planned as a prototype.

## ER Schema

The following ER schema has been developed:![er_schema](https://user-images.githubusercontent.com/13967444/163443220-3d36cb1a-63f4-43e0-9938-d8afbe544c8f.svg)


## Backend

The backend will be devloped in Python using the Django framework.
