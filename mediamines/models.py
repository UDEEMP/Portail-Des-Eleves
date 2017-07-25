import os
from django.db import models

from trombi.models import UserProfile
from portail import settings
from django.core.files import File
from django.forms import ModelForm, DateInput
from imagekit.models import ImageSpecField

from imagekit.processors import ResizeToFill
from dal import autocomplete
from datetime import datetime

PRIX_PHOTO = 0.5

class Gallerie(models.Model):

    nom = models.CharField(max_length=128, verbose_name="Nom de la gallerie", default="Nom par défaut")
    nom_dossier = models.CharField(max_length=50, verbose_name="Nom du dossier, unique", unique=True, default="nom_defaut")
    description = models.CharField(max_length=528, verbose_name="Description de la gallerie", null=True, blank=True)

    """ debut|fin chrono servent à cadrer la période que concerne les photos. Optionnel, peut permettre tri."""
    dateCreation = models.DateField(default=datetime.now())
    dateDebutChrono = models.DateField(blank=True, null=True, default=None)
    dateFinChrono = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return self.nom

class Photo(models.Model):


    def getImagePath(self, filename):
        return 'mediamines/gallerie_{0}/{1}'.format(self.gallerie.nom_dossier, filename)
    def delete(self):
        os.remove(self.image_thumbnail_1.path)
        self.image.delete()
        # Attention, les thumbnails ne sont pas supprimées à l'issu de delete
        # Il faut appeler imagekit.utils.get_cache().clear()
        super(Photo, self).delete()

    description = models.CharField(max_length=528, verbose_name="Description de la photo", null=True, blank=True)
    identifications = models.ManyToManyField(UserProfile, null=True, blank=True)
    gallerie = models.ForeignKey(Gallerie, null=True, blank=True)

    image = models.ImageField(upload_to=getImagePath, null=True, blank=True)
    image_thumbnail_1 = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 50)])

    dateUpload = models.DateField(default=datetime.now())



class AppreciationPhoto(models.Model):
    isLike = models.BooleanField(verbose_name="Like it ?", default=True)
    userProfile = models.ForeignKey(UserProfile, null=True, blank=True )
    photo = models.ForeignKey(Photo, null=True, blank=True)
    date = models.DateField(default=datetime.now())

class DemandeImpression(models.Model):
    userProfile = models.ForeignKey(UserProfile, null=True, blank=True)
    quantite = models.IntegerField(default=0)
    photo = models.ForeignKey(Photo, null=True, blank=True)
    dateDemande = models.DateField(default=datetime.now())
    dateTraitee = models.DateField(blank=True, null=True, default=None) # Sert à filtrer les tirages déjà effectués
    deletedByUser = models.BooleanField(default=False)
    deletedByMediamine = models.BooleanField(default=False)
    prix = models.FloatField(default=0) # Une autre sécurité
    wasEncaissee = models.BooleanField(default=False) # Juste une sécurité
    taille = models.IntegerField(default=0) # A relier à un tableau des tailles
    # AJOUTER TAILLE

    def isDeleted(self):
        return self.deletedByUser or self.deletedByMediamine
    def isVisibleInDemandsList(self):
        return not(self.isDeleted) and self.dateTraitee is None

    """
    BITE
    """

class PhotoUploadSingleForm(ModelForm):
    #identifications = ModelMultipleChoiceField(required=False,widget=autocomplete.ModelSelect2Multiple(url="trombi-autocomplete"), queryset=UserProfile.objects.all())
    class Meta:
        model = Photo
        #options = {'size': (300, 100), 'crop': True}
        exclude = ('image_thumbnail_1','gallerie', 'dateUpload')
        widgets = {
            'identifications': autocomplete.ModelSelect2Multiple("trombi-autocomplete"),
        }

class PhotoModifForm(ModelForm):
    class Meta:
        model = Photo
        #options = {'size': (300, 100), 'crop': True}
        exclude = ('image_thumbnail_1','image', 'dateUpload', 'gallerie')
        widgets = {
            'identifications': autocomplete.ModelSelect2Multiple("trombi-autocomplete"),
        }

class GallerieForm(ModelForm):
    class Meta:
        model = Gallerie
        exclude = ('dateCreation',)
        widgets = {
            'dateDebutChrono': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}),
            'dateFinChrono': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}),
        }