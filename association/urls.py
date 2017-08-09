#-*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic import TemplateView
from evenement import views as evenement_views
from association import views as ass_views
from django.contrib.auth.decorators import login_required
from message import views as message_views
# Views d'autres modules
urlpatterns = [
    url(r'^(?P<association_pseudo>\w+)/messages/poster_message/$', message_views.nouveau),
    url(r'^(?P<association_pseudo>\w+)/evenements/nouveau/$', evenement_views.nouveau),
    url(r'^trium/informations/$', TemplateView.as_view(template_name='trium/informations.html')),
    url(r'^wei/teaser/$', TemplateView.as_view(template_name='wei/teaser.html')),
    url(r'^minestryofsound/', include('minestryofsound.urls')),
    url(r'^minesmarket/', include('minesmarket.urls')),
    url(r'^freshbox/', include('freshbox.urls')),
    #url(r'^mediamines_old/', include('mediamines_old.urls')),
    url(r'^paindemine/', include('paindemine.urls')),
    url(r'^abatage/', include('abatage.urls')),
    url(r'^vendome/', include('vendome.urls')),
    url(r'^bde/', include('bde.urls')),
    url(r'^bda/', include('bda.urls')),
    url(r'^bds/', include('bds.urls')),
    url(r'^htc/', include('htc.urls')),
    #url(r'^psl/', include('psl.urls')),
    url(r'^pr/', include('pr.urls')),
    url(r'^mineshake/', include('mineshake.urls')),
    url(r'^S3/', include('S3.urls')),
    url(r'^radiopsl/', include('radiopsl.urls')),
    url(r'^bapteme/', include('bapteme.urls')),
    url(r'^bdtek/', include('bdtek.urls'))
]

# Views du module association
urlpatterns += [
    url(r'^$', ass_views.index, name='associations'),
    url(r'^(?P<association_pseudo>\w+)/$', ass_views.description),
    url(r'^(?P<association_pseudo>\w+)/equipe/$', ass_views.equipe),
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_ordre/$', ass_views.changer_ordre),    
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_role/(?P<eleve_id>\d+)$', ass_views.changer_role),    
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_role/$', ass_views.changer_role, {'eleve_id':None}),    
    url(r'^(?P<association_pseudo>\w+)/equipe/ajouter_membre/$', ass_views.ajouter_membre),
    url(r'^(?P<association_pseudo>\w+)/equipe/supprimer_membre/$', ass_views.supprimer_membre),
    url(r'^(?P<association_pseudo>\w+)/messages/$', ass_views.messages),
    url(r'^(?P<association_pseudo>\w+)/evenements/$', ass_views.evenements),
    url(r'^(?P<association_pseudo>\w+)/medias/$', ass_views.medias, name='association_medias'),
    url(r'^(?P<association_pseudo>\w+)/medias/video/ajouter/$', ass_views.ajouter_video),
    url(r'^(?P<association_pseudo>\w+)/medias/video/(?P<video_id>\d+)/supprimer/$', ass_views.supprimer_video),
    url(r'^(?P<association_pseudo>\w+)/medias/affiche/ajouter/$', ass_views.ajouter_affiche),
    url(r'^(?P<association_pseudo>\w+)/medias/affiche/(?P<affiche_id>\d+)/supprimer/$', ass_views.supprimer_affiche),
    url(r'^(?P<association_pseudo>\w+)/description/$', ass_views.description, name="description_asso"),
    url(r'^(?P<association_pseudo>\w+)/editDescription/$', ass_views.changeDescription, name="edit_description"),

    url(r'^(?P<association_pseudo>\w+)/news/$', ass_views.getNews, name="news_liste"),
    url(r'^(?P<association_pseudo>\w+)/news/add/$', login_required(ass_views.AjouterNews.as_view()), name="add_news"),
    url(r'^(?P<association_pseudo>\w+)/news/change/(?P<pk>\d+)$', login_required(ass_views.ModifierNews.as_view()), name="change_news"),
    url(r'^(?P<association_pseudo>\w+)/news/delete/(?P<pk>\d+)$', login_required(ass_views.SupprimerNews.as_view()), name="delete_news")

]
