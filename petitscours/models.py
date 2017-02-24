# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from notification.models import Notification, Envoi
from association.models import Association
from django.contrib.contenttypes import fields

#Une proposition de petit cours
class PetitCours(models.Model):
    poste_par = models.ForeignKey(User, related_name='petits_cours_postes', blank=True, null=True) #L'eleve qui a post� le petit cours
    title = models.CharField(max_length=256)
    contact = models.CharField(max_length=256) #Num�ro de t�l�phone ?
    date_added = models.DateTimeField(auto_now_add=True)
    date_given = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField()
    niveau = models.CharField(max_length=256)
    frequence = models.CharField(max_length=256)
    disponibilite = models.CharField(max_length=256)
    prenom = models.CharField(max_length=256)
    age = models.CharField(max_length=256)
    matiere = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    requests = models.ManyToManyField(User,related_name='+', blank=True) #Les demandes
    attribue_a = models.ForeignKey(User, related_name='petits_cours_attribues', blank=True, null=True) #L'eleve a qui le pc est attribu�

    address = models.CharField(max_length=500, null=True) #Adresse � Paris (via l'API Google Maps)
    latitude = models.FloatField(null=True) #r�cup�r�e dynamiquement via l'API Google Maps
    longitude = models.FloatField(null=True) #r�cup�r�e dynamiquement via l'API Google Maps

    notification = fields.GenericRelation(Notification)

    visible.default = True

    class Meta:
        verbose_name_plural = "petits cours"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/petitscours/'

    #Met � jour la position GPS du petit cours. Appel� depuis l'API Google Maps.
    def update_location(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def envoyer_notification(self):
        try:
            bde = Association.objects.get(pseudo='bde') #On envoie seulement � ceux qui suivent le BDE
            notification = Notification(content_object=self, description='Un nouveau petit cours est disponible')
            notification.save()
            notification.envoyer_multiple(bde.suivi_par.all())
        except Association.DoesNotExist:
            pass


    def save(self, *args, **kwargs):
        creation = self.pk is None #Creation de l'objet
        super(PetitCours, self).save(*args, **kwargs)
        if creation:
            self.envoyer_notification()
