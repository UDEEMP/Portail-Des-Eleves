from django.conf.urls import url
from mediamines import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', views.interfaceAdminMediamine, name='interface_mediamines'),

    #url(r'^gallerie/modifier/?$', views.interfaceAdminMediamine),
    url(r'^admin/gallerie/ajouter/$', login_required(views.AjouterGallerie.as_view()), name="ajouter_gallerie"),
    url(r'^admin/gallerie/modifier/(?P<pk>\d+)$', login_required(views.ModifierGallerie.as_view()), name="modifier_gallerie"),
    url(r'^admin/gallerie/supprimer/(?P<pk>\d+)$', login_required(views.SupprimerGallerie.as_view()), name="supprimer_gallerie"),

    url(r'^admin/gallerie/(?P<gallery_id>\d+)/$', views.interfaceGallerieMediamine, name="interface_photo_gallerie"),
    url(r'^admin/gallerie/(?P<gallery_id>\d+)/ajouterPhotoSingle$', login_required(views.AjouterPhotoSingle.as_view()), name="ajouter_photo_single"),
    url(r'^admin/gallerie/(?P<gallery_id>\d+)/ajouterPhotoMultiple$', login_required(views.AjouterPhotoMultiple.as_view()), name="ajouter_photo_multiple"),

    url(r'^gallerie/$', views.client_gallerie_liste, name="client_galleries"),

    url(r'^admin/photo/modifier/(?P<pk>\d+)$', login_required(views.ModifierPhoto.as_view()), name="modifier_photo"),
    url(r'^admin/photo/supprimer/(?P<pk>\d+)$', login_required(views.SupprimerPhoto.as_view()), name="supprimer_photo"),

    url(r'^photo/demandeTirage/(?P<photo_id>\d+)$', views.demanderImpression, name="demander_photo"),
    url(r'^photo/view/(?P<pk>\d+)$', login_required(views.ClientViewPhoto.as_view()), name="view_photo"),
    url(r'^photo/view/(?P<pk>\d+)/(?P<demande>[^/]+)$', login_required(views.ClientViewPhoto.as_view()), name="view_photo_demande"),
    url(r'^photo/appreciation/(?P<photo_id>\d+)/(?P<is_like>[^/]+)$', views.client_appreciation_photo, name="appreciation_photo"),


    url(r'^admin/recap/generate/$', views.generateRecapImpression, name="generate_recap"),
    url(r'^admin/recap/zip/(?P<recap_id>\d+)$', views.generateOrDeleteZips, name="change_zip_recap"),
    url(r'^admin/recap/debiteOrAnnule/(?P<recap_id>\d+)$', views.debiteOrAnnuleRecap, name="debite_or_annule_recap"),
    url(r'^admin/recap/cancel/(?P<recap_id>\d+)$', views.cancelRecap, name="cancel_recap"),
    url(r'^admin/recap/changeArchivage/(?P<recap_id>\d+)$', views.changeArchivageRecap, name="change_archivage_recap"),
    url(r'^admin/recap/details/(?P<recap_id>\d+)$', views.detailRecap, name="details_recap"),


    url(r'^admin/solde/modifier$', login_required(views.modifierSolde.as_view()), name="modifier_solde"),
    url(r'^admin/solde/afficher$', views.afficherSoldes, name="afficher_soldes"),

    #url(r'^cache_clear', views.cache_clear, name="cache_clear"),

    #url(r'^newsletter/json/$', views.newsletter_json, name='newsletter_json'),
]