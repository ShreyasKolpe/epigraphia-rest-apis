"""epigraphia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apis import views

urlpatterns = [
    path('source_text', views.SourceTextView.as_view()),
    path('source_text/<int:text_id>', views.SourceTextView.as_view()),

    path('source_text_chapter', views.SourceTextChapterView.as_view()),
    path('source_text_chapter/<int:chapter_id>', views.SourceTextChapterView.as_view()),
    path('source_text_chapter/search', views.get_source_text_chapters_by_search),

    path('location', views.LocationView.as_view()),
    path('location/<int:location_id>', views.LocationView.as_view()),

    path('inscription', views.InscriptionView.as_view()),
    path('inscription/<int:inscription_id>', views.InscriptionJoinedView.as_view()),
    path('inscription/search', views.get_inscriptions_by_search),
]
