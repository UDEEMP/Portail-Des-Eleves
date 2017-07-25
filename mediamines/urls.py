from django.conf.urls import url
from mediamines import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', views.interfaceAdminMediamine, name='interface_mediamines'),

    #url(r'^gallerie/modifier/?$', views.interfaceAdminMediamine),
    url(r'^gallerie/ajouter/$', login_required(views.AjouterGallerie.as_view()), name="ajouter_gallerie"),
    url(r'^gallerie/modifier/(?P<pk>\d+)$', login_required(views.ModifierGallerie.as_view()), name="modifier_gallerie"),
    url(r'^gallerie/supprimer/(?P<pk>\d+)$', login_required(views.SupprimerGallerie.as_view()), name="supprimer_gallerie"),

    url(r'^gallerie/(?P<gallery_id>\d+)/$', views.interfaceGallerieMediamine, name="interface_photo_gallerie"),
    url(r'^gallerie/(?P<gallery_id>\d+)/ajouterPhotoSingle$', login_required(views.AjouterPhotoSingle.as_view()), name="ajouter_photo_single"),

    url(r'^photo/modifier/(?P<pk>\d+)$', login_required(views.ModifierPhoto.as_view()), name="modifier_photo"),
    url(r'^photo/supprimer/(?P<pk>\d+)$', login_required(views.SupprimerPhoto.as_view()), name="supprimer_photo"),

    #url(r'^cache_clear', views.cache_clear, name="cache_clear"),

    #url(r'^newsletter/json/$', views.newsletter_json, name='newsletter_json'),
]