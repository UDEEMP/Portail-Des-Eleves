import os

import zipfile
from django.db import models

from trombi.models import UserProfile

from portail import settings
from django.core.files import File
from django.forms import ModelForm, DateInput, Form
import django.forms as forms
from imagekit.models import ImageSpecField

from imagekit.processors import ResizeToFit
from dal import autocomplete
from datetime import datetime
from multiupload.fields import MultiImageField
from django.forms.fields import ImageField
import mediamines.tools as tools

PRIX_PAR_FORMAT = [0.5, 1]
NOM_PAR_FORMAT = ["Normal", "Grande"]
DISPLAY_PRIORITY_NORMAL = 0
DISPLAY_PRIORITY_MINIATURE = 1
DISPLAY_PRIORITY_REPRESENTANT = 2


class Gallerie(models.Model):

    class Meta:
        permissions = (
            ("gestion_gallerie", "Peut administrer les galleries"),
        )

    nom = models.CharField(max_length=128, verbose_name="Nom de la gallerie", default="Nom par défaut")
    nom_dossier = models.CharField(max_length=50, verbose_name="Nom du dossier, unique", unique=True, default="nom_defaut")
    description = models.CharField(max_length=528, verbose_name="Description de la gallerie", null=True, blank=True)

    """ debut|fin chrono servent à cadrer la période que concerne les photos. Optionnel, peut permettre tri."""
    dateCreation = models.DateField(default=datetime.now())
    dateDebutChrono = models.DateField(blank=True, null=True, default=None)
    dateFinChrono = models.DateField(blank=True, null=True, default=None)

    isHiddenFrom1A = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    def delete(self):
        for photo in self.photo_set.all():
            photo.delete()
        super(Gallerie, self).delete()

    def get_photo_representative(self):
        lastest = None
        for photo in self.photo_set.all():
            if photo.displayPriority == DISPLAY_PRIORITY_REPRESENTANT:
                return photo
            lastest = photo
        return lastest

    def get_photos_miniatures(self):
        photos = []
        for photo in self.photo_set.all():
            if photo.displayPriority == DISPLAY_PRIORITY_MINIATURE:
                photos.append(photo)
        return photos

    def get_photos_in_order(self):
        photos = self.photo_set.all().order_by("-displayPriority", "-dateUpload")
        return photos


    def get_photo_with_delta(self, id_photo, delta):
        photos = self.get_photos_in_order()
        if(photos.count() <= 0):
            return None
        nbr = 0
        for i in range(photos.count()):
            if photos[i].id == id_photo:
                nbr = i

        next_nbr = (nbr + delta) % photos.count()
        return photos[next_nbr]

    def get_next_photo(self, id_photo):
        return self.get_photo_with_delta(id_photo, +1)
    def get_previous_photo(self, id_photo):
        return self.get_photo_with_delta(id_photo, -1)


class Photo(models.Model):

    class Meta:
        permissions = (
            ("gestion_photo", "Peut administrer les photos"),
        )

    # Regenerer les templates si introuvables
    # IMPORTANT !!!


    def getImagePath(self, filename):
        return 'mediamines/gallerie_{0}/{1}'.format(self.gallerie.nom_dossier, filename)
    def delete(self):
        os.remove(self.image_thumbnail_1.path)
        os.remove(self.image_thumbnail_2.path)
        self.imageOriginale.delete()
        super(Photo, self).delete()

    description = models.CharField(max_length=528, verbose_name="Description de la photo", null=True, blank=True)
    identifications = models.ManyToManyField(UserProfile, null=True, blank=True, related_name="identifications")
    gallerie = models.ForeignKey(Gallerie, null=True, blank=True)


    # Originale, petite miniature, moyenne miniature
    image = models.ImageField(upload_to=getImagePath, null=True, blank=True)
    image_thumbnail_1 = ImageSpecField(source='image',
                                      processors=[ResizeToFit(360, 200)])
    image_thumbnail_2 = ImageSpecField(source='image',
                                       processors=[ResizeToFit(720, 480, False)])

    #image_thumbnail_1 = ImageSpecField(source='image',
                                       #processors=[ResizeToFill(100, 50)])

    dateUpload = models.DateField(default=datetime.now())
    uploader = models.ForeignKey(UserProfile, null=True, blank=True, related_name="uploader")

    displayPriority = models.IntegerField(default=-10)
    # 0 = normal, 1 = miniature de gallerie, 2 = photo d'affiche


    def getImageName(self):
        return os.path.basename(self.image.path)


class HistoriqueActions(models.Model):
    mediamine_user = models.ForeignKey(UserProfile, null=True, blank=True, related_name="mediamine_user")
    texte = models.CharField(max_length=500)
    sommeDebitee = models.FloatField(default=0)
    client = models.ForeignKey(UserProfile, null=True, blank=True, related_name="client")
    date = models.DateField(default=datetime.now())


class AppreciationPhoto(models.Model):
    isLike = models.BooleanField(verbose_name="Like it ?", default=True)
    userProfile = models.ForeignKey(UserProfile, null=True, blank=True )
    photo = models.ForeignKey(Photo, null=True, blank=True)
    date = models.DateField(default=datetime.now())

class DemandeImpression(models.Model):
    userProfile = models.ForeignKey(UserProfile, null=True, blank=True)
    #quantite = models.IntegerField(default=0)
    photo = models.ForeignKey(Photo, null=True, blank=True)
    dateDemande = models.DateField(default=datetime.now())
    dateTraitee = models.DateField(blank=True, null=True, default=None) # Sert à filtrer les tirages déjà effectués
    deletedByUser = models.BooleanField(default=False)
    deletedByMediamine = models.BooleanField(default=False)
    prix = models.FloatField(default=0) # Une autre sécurité
    wasEncaissee = models.BooleanField(default=False) # Juste une sécurité
    taille = models.IntegerField(default=0) # A relier à un tableau des tailles

    objects = models.Manager()

    # AJOUTER TAILLE

    @staticmethod
    def get_en_attente():
        demandes = DemandeImpression.objects.all()
        count = 0
        to_be_deleted = []
        for demande in demandes:
            if (demande.enAttente() and demande.userProfile.has_enough_money_for_mediamines_commande()):
                count += 1
            else:
                to_be_deleted.append(demande.id)
        return demandes.exclude(id__in=to_be_deleted)



    def isDeleted(self):
        return self.deletedByUser or self.deletedByMediamine
    def enAttente(self):
        return not(self.isDeleted()) and self.dateTraitee is None
    def isVisibleInDemandsList(self):
        return self.enAttente()

    def get_str_for_taille(self):
        return NOM_PAR_FORMAT[self.taille]


class RecapitulatifImpressions(models.Model):
    mediamine_user = models.ForeignKey(UserProfile, null=True, blank=True)
    demandes = models.ManyToManyField(DemandeImpression, null=True, blank=True)
    dateGeneration = models.DateField(default=datetime.now())
    zipPhotos = models.FileField(null=True, blank=True)
    zipMiniatures = models.FileField(null=True, blank=True)
    hasDebited = models.BooleanField(default=False) # Débite les gens concernés
    isCanceled = models.BooleanField(default=False) # Annulation, peut toujours servir
    isArchived = models.BooleanField(default=False) # Archivage pour pas tout afficher


    class Meta:
        permissions = (
            ("gestion_recap", "Peut administrer les recaps & les soldes"),
        )

    @staticmethod
    def generateRecap(profile):
        """demandes = DemandeImpression.objects.all()
        # On ne conserve que les demandes encore en attente avec des utilisateurs qui ont l'argent pour leur commande
        count = 0
        to_be_deleted = []
        for demande in demandes:
            if(demande.enAttente() and demande.userProfile.has_enough_money_for_mediamines_commande()):
                demande.dateTraitee = datetime.now()
                demande.save()
                count+=1
            else:
                to_be_deleted.append(demande.id)
        if(count > 0):
            recap = RecapitulatifImpressions.objects.create(mediamine_user=profile)
            recap.demandes = demandes.exclude(id__in=to_be_deleted)
            return recap
        return None"""

        demandes = DemandeImpression.get_en_attente()
        if(demandes.count() > 0):
            recap = RecapitulatifImpressions.objects.create(mediamine_user=profile)
            recap.demandes = demandes
            for demande in demandes:
                demande.dateTraitee = datetime.now()
                demande.save()
            return recap
        return None

        #return RecapitulatifImpressions.objects.create(mediamine_user = profile, demandes=demandes)


    def debiteOrAnnule(self, profile, isDebite):
        multiplier = 1
        if(not(isDebite)):
            multiplier = -1
        header = "debite"
        if (not (isDebite)):
            header = "annule"

        for demande in self.demandes.all():
            if not(demande.wasEncaissee == isDebite):
                demande.wasEncaissee = isDebite
                prix = multiplier * demande.prix
                demande.userProfile.update_solde_mediamines(prix)
                HistoriqueActions.objects.create(
                    mediamine_user=profile,
                    texte = header + " recap " + self.id.__str__() + ", demande " + demande.id.__str__() +", débite "+ prix.__str__(),
                    sommeDebitee = prix,
                    client = demande.userProfile
                )
                demande.save()
        self.hasDebited = isDebite
        self.save()

    def debite(self, profile):
        self.debiteOrAnnule(profile, True)

    def annule(self, profile):
        self.debiteOrAnnule(profile, False)

    def cancel(self, profile):
        self.annule(profile)
        for demande in self.demandes.all():
            demande.dateTraitee = None
            demande.save()
        self.isCanceled = True
        self.save()

    def generateZipImages(self):
        pathFromMediaRoot = "mediamines/zip/recap_originales_"+self.id.__str__()+".zip"
        pathToZip = os.path.join(settings.MEDIA_ROOT, pathFromMediaRoot)
        """pathToTempFolder = os.path.join(settings.MEDIA_ROOT, "mediamines/zip/temporaire/recap_"+self.id.__str__()+"/")
        pathToImages = os.path.join(pathToTempFolder, "originales")
        pathToMiniatures = os.path.join(pathToTempFolder, "miniatures")"""

        #os.close(os.open(pathToZip, 'wb'))
        if(not(os.path.exists(os.path.dirname(pathToZip)))):
            os.makedirs(os.path.dirname(pathToZip))

        #open(pathToZip, 'wb').close()

        with zipfile.ZipFile(pathToZip, 'w') as zf:

            for demande in self.demandes.all():
                pathForThisDemande = os.path.join(
                    NOM_PAR_FORMAT[demande.taille],
                    "TIRAGE_"+demande.userProfile.user.username+"_demande"+demande.id.__str__()+"_"+NOM_PAR_FORMAT[demande.taille]+"_photo"+demande.photo.id.__str__()+"_"+demande.photo.getImageName())
                zf.write(demande.photo.image.path, pathForThisDemande)
            zf.close()
            self.zipPhotos.name = pathFromMediaRoot
            self.save()

    def generateZipMiniatures(self):
        pathFromMediaRoot = "mediamines/zip/recap_miniatures_"+self.id.__str__()+".zip"
        pathToZip = os.path.join(settings.MEDIA_ROOT, pathFromMediaRoot)
        """pathToTempFolder = os.path.join(settings.MEDIA_ROOT, "mediamines/zip/temporaire/recap_"+self.id.__str__()+"/")
        pathToImages = os.path.join(pathToTempFolder, "originales")
        pathToMiniatures = os.path.join(pathToTempFolder, "miniatures")"""

        #os.close(os.open(pathToZip, 'wb'))
        if(not(os.path.exists(os.path.dirname(pathToZip)))):
            os.makedirs(os.path.dirname(pathToZip))

        #open(pathToZip, 'wb').close()

        with zipfile.ZipFile(pathToZip, 'w') as zf:

            for demande in self.demandes.all():
                pathForThisDemande = os.path.join(
                    demande.userProfile.user.username,
                    "MINIATURE_"+demande.userProfile.user.username+"_demande"+demande.id.__str__()+"_"+NOM_PAR_FORMAT[demande.taille]+"_photo"+demande.photo.id.__str__()+"_"+demande.photo.getImageName())
                zf.write(demande.photo.image_thumbnail_1.path, pathForThisDemande)
            zf.close()
            self.zipMiniatures.name = pathFromMediaRoot
            self.save()

    def delete_zips(self):
        if(bool(self.zipMiniatures) and os.path.isfile(self.zipMiniatures.path)):
            os.remove(self.zipMiniatures.path)
        if(bool(self.zipPhotos) and os.path.isfile(self.zipPhotos.path)):
            os.remove(self.zipPhotos.path)
        self.zipMiniatures = None
        self.zipPhotos = None
        self.save()

    def generateOrDeleteZips(self):
        if(not(bool(self.zipMiniatures)) or not(bool(self.zipPhotos))):
            self.generateZipImages()
            self.generateZipMiniatures()
        else:
            self.delete_zips()


    def archiveOrDesarchive(self):
        self.delete_zips()
        self.isArchived = not(self.isArchived)
        self.save()


    def get_string_for_zip_action(self):
        if (bool(self.zipMiniatures) and bool(self.zipPhotos)):
            return "Supprimer"
        else:
            return "Générer"

    def get_string_archivage(self):
        if self.isArchived:
            return "Désarchiver"
        else:
            return "Archiver"

    def get_string_debit(self):
        if self.hasDebited:
            return "Rembourser"
        else:
            return "Débiter"

    def get_prix_total(self):
        somme = 0
        for demande in self.demandes.all():
            somme += demande.prix
        return somme

    def get_demandes_by_user(self):
        dic = {}
        users = []
        for demande in self.demandes.all():
            if not(demande.userProfile in users):
                users.append(demande.userProfile)

        for profile in users:
            dic[profile] = self.demandes.filter(userProfile=profile)
        return dic


    def get_prix_total_for_client(self, profile):
        somme = 0
        for demande in self.demandes.filter(userProfile=profile):
            somme += demande.prix
        return somme

class PhotoUploadSingleForm(ModelForm):
    #identifications = ModelMultipleChoiceField(required=False,widget=autocomplete.ModelSelect2Multiple(url="trombi-autocomplete"), queryset=UserProfile.objects.all())
    image = ImageField()
    class Meta:
        model = Photo
        #options = {'size': (300, 100), 'crop': True}
        exclude = ('image_thumbnail_1','image_thumbnail_2', 'gallerie', 'dateUpload', 'uploader')
        widgets = {
            'identifications': autocomplete.ModelSelect2Multiple("trombi-autocomplete"),
        }
class PhotoUploadMultiForm(Form):
    fichiers = MultiImageField(min_num=1, max_num=100, max_file_size=1024*1024*6)

class PhotoModifForm(ModelForm):
    CHOICES = (
        ("-10", "Normal"),
        ("1", "Miniature"),
        ("2", "Couverture"),
        ("-5", "Haut de gallerie")
    )

    displayPriority = forms.ChoiceField(label="Priorité d'affichage", widget=forms.Select, choices=CHOICES)

    class Meta:
        model = Photo

        #options = {'size': (300, 100), 'crop': True}
        exclude = ('image_thumbnail_1', 'image_thumbnail_2', "image", 'dateUpload', 'gallerie', 'uploader')
        widgets = {
            'identifications': autocomplete.ModelSelect2Multiple("trombi-autocomplete"),
        }

class PhotoIdentificationForm(ModelForm):
    class Meta:
        model = Photo
        #options = {'size': (300, 100), 'crop': True}
        fields = ['identifications']
        widgets = {
            'identifications': autocomplete.ModelSelect2Multiple("trombi-autocomplete"),
        }

class PhotoImpressionForm(ModelForm):

    CHOICES = False
    for i in range(len(NOM_PAR_FORMAT)):
        if not (CHOICES):
            CHOICES = (i.__str__(), NOM_PAR_FORMAT[i] + ", " + PRIX_PAR_FORMAT[i].__str__() + "€")
        else:
            CHOICES = (CHOICES,) + ((i.__str__(), NOM_PAR_FORMAT[i] + ", " + PRIX_PAR_FORMAT[i].__str__() + "€"),)

    if not (CHOICES):
        CHOICES = ()

    taille = forms.ChoiceField(widget=forms.Select, choices=CHOICES)


    class Meta:
        model = DemandeImpression
        fields = ['taille']

class GallerieForm(ModelForm):
    class Meta:
        model = Gallerie
        exclude = ('dateCreation',)
        widgets = {
            'dateDebutChrono': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}),
            'dateFinChrono': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}),
        }


class SoldeModifForm(forms.Form):
    client = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=autocomplete.ModelSelect2("trombi-autocomplete"))
    credit = forms.FloatField()
