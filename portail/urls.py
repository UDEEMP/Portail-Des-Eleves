from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import os
from trombi import views as trombi_views
from entreprise import views as entreprise_views
from petitscours import views as petitscours_views
from objettrouve import views as objettrouve_views
from recherche import views as recherche_views
from notification import views as notification_views
from intranetlink import views as intranetlink_views
from availableClassrooms import views as availableClassrooms_views
from message import views as message_views
#oneY1B_views = __import__('1y1b.views')


admin.autodiscover()

urlpatterns = [

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/?', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', trombi_views.profile),
    #url(r'^sso/1y1b/authentication$', oneY1B_views.connection),
    #url(r'^sso/1y1b/authentication_accueil$', oneY1B_views.connection_accueil),
    #url(r'^sso/1y1b/authentication_accueil/', oneY1B_views.connection_accueil),
    #url(r'^sso/1y1b/logout$', oneY1B.views.logout_view),
    #url(r'^yearbook/$', '1y1b.views.yearbook'),
    url(r'^token/$', trombi_views.token),
    url(r'^comments/post/$', message_views.post_comment ),
    url(r'^comments/delete/$', message_views.delete_own_comment ),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^people/', include('trombi.urls')),
    url(r'^messages/', include('message.urls')),
    url(r'^sondages/', include('sondages.urls')),
    url(r'^timetable/', include('timetable.urls')),
    url(r'^evenements/', include('evenement.urls')),
    url(r'^entreprises/', include('entreprise.urls')),
    url(r'^entreprises/contact_accueil/$', entreprise_views.contact_entreprises_accueil),
    url(r'^entreprises/accueil/$', entreprise_views.presentation_entreprises_accueil),
    url(r'^entreprises/planning_accueil/$', entreprise_views.planning_accueil),
    url(r'^petitscours/', include('petitscours.urls')),
    url(r'^petitscours/demander/accueil/$', petitscours_views.demander_accueil),
    url(r'^associations/', include('association.urls')),
    url(r'^objetstrouves/?$',objettrouve_views.index),
    url(r'^objetstrouves/ajouter/?$',objettrouve_views.ajouter),
    url(r'^objetstrouves/supprimer/?$',objettrouve_views.supprimer),
    url(r'^bilanmandat/', include('bilanmandat.urls')),
    url(r'^recherche/?$',recherche_views.search),
    url(r'^notifications/$', notification_views.liste),
    url(r'^notifications/preferences/$', notification_views.preferences),
    url(r'^chat/', include('chat.urls')),
    #url(r'^tinymce/', include('tinymce.urls')),
    #url(r'^accueil/?$','messages.views.index'),
    url(r'^accueil/?$',trombi_views.profile),
    #url(r'^trombiassos/?$','trombiassos.views.trombi_assos'),
    #url(r'^trombiassos1/?$','trombiassos.views.trombi_assos1'),
    #url(r'^trombiassos2/?$','trombiassos.views.trombi_assos2'),
    #url(r'^trombiassos3/?$','trombiassos.views.trombi_assos3'),
    #url(r'^trombiassos1fant/?$','trombiassos.views.trombi_assos1fant'),
    #url(r'^trombiassos2fant/?$','trombiassos.views.trombi_assos2fant'),
    #url(r'^trombiassos3fant/?$','trombiassos.views.trombi_assos3fant'),
    #url(r'^trombiassos4/?$','trombiassos.views.trombi_assos4'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    #url(r'^/?$','messages.views.index'),
    url(r'^/?$',trombi_views.profile),
    url(r'^2048/',include('2048.urls')),
    url(r'^xml/evenements.xml',intranetlink_views.getEvents),
    url(r'^availableClassrooms/$', availableClassrooms_views.availableClassrooms),
    url(r'^availableClassrooms/classrooms.dat$', availableClassrooms_views.getData)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
