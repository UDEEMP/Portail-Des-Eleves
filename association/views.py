#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView

from association.models import Association, Adhesion, Affiche, Video, AdhesionAjoutForm, AdhesionModificationForm, \
    AdhesionSuppressionForm, AfficheForm, VideoForm, News
from association.models import DescriptionForm, NewsForm
from evenement.models import Evenement
from message.models import Message


@login_required
# La liste de toutes les associations
def index(request):
    assoces = Association.objects.order_by('ordre');
    if request.user.profile.en_premiere_annee():
        assoces = assoces.exclude(is_hidden_1A = True)
    assoces = assoces.exclude(ordre__lt = 0)
    return render(request, 'association/index.html', {'assoces' : assoces})

@login_required
# La liste des membres d'une association
def equipe(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    return render(request, 'association/equipe.html', {'association' : association, 'membres': membres})

@login_required
# Les messages postés par une association
def messages(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    list_messages = Message.accessibles_par(request.user.profile).filter(association__pseudo=association_pseudo).order_by('-date')
    return render(request, 'association/messages.html', {'association' : association, 'list_messages': list_messages, 'membres': membres})




@login_required
# Les événements planifiés par une association
def evenements(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    liste_evenements = Evenement.objects.filter(association__pseudo=association_pseudo).order_by('-date_debut')

    return render(request, 'association/evenements.html', {'association' : association, 'liste_evenements': liste_evenements, 'membres': membres})
@login_required
# Les événements planifiés par une association
def medias(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    liste_affiches = Affiche.objects.filter(association__pseudo=association_pseudo)
    liste_videos = Video.objects.filter(association__pseudo=association_pseudo)

    return render(request, 'association/medias.html', {'association' : association, 'liste_affiches': liste_affiches, 'liste_videos': liste_videos, 'membres': membres})    
@login_required    
# Ajouter un membre à une association
def ajouter_membre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    if request.method == 'POST': 
        form = AdhesionAjoutForm(assoce, request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            fonction = form.cleaned_data['role']
            if Adhesion.objects.filter(association=assoce, eleve_id=request.user.profile.id).exists(): #Si l'eleve est membre de l'assoce
                Adhesion.objects.create(eleve=utilisateur, association=assoce, role=fonction)
            return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/')
    else:
        form = AdhesionAjoutForm(assoce) # formulaire vierge

    return render(request, 'association/admin.html', {'form': form,})
@login_required    
# Changer le rôle d'un membre à une association
def changer_role(request, association_pseudo, eleve_id):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    #On vérifie que l'association n'est pas cachée au membre.
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    #On vérifie que l'utilisateur fait partie de l'association
    if not membres.filter(eleve_id=request.user.profile.id).exists():
        return render(request, 'association/equipe.html', {'association' : association, 'membres': membres})    
    #Si on a choisi un élève à modifier
    if eleve_id:

        #On récupère l'élève à modifier ou on redirige vers la page de l'équipe
        try:
            eleve = membres.get(id=eleve_id)
        except Adhesion.DoesNotExist:
            return render(request, 'association/equipe.html', {'changer_role':True, 'association' : association, 'membres': membres})
        if request.method == 'POST':
            form = AdhesionModificationForm(request.POST)
            if form.is_valid():
                #On modifie le rôle et on redirige
                eleve.role = form.cleaned_data['role']
                eleve.save()
                return HttpResponseRedirect('/associations/' + association_pseudo + '/equipe/')
        else:
            form = AdhesionModificationForm({'role':eleve.role})
        #On envoie sur la page du formulaire
        return render(request, 'association/admin.html', {'changer_role':True, 'form':form, 'association' : association, 'membres': membres})
    else:
        #On envoie sur la page avec la présentation de l'équipe ET des liens pour modifier.
        return render(request, 'association/equipe.html', {'changer_role':True, 'association' : association, 'membres': membres})    
    
@login_required    
# Supprimer un membre d'une association
def supprimer_membre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    if request.method == 'POST': 
        form = AdhesionSuppressionForm(assoce, request.POST) 
        if form.is_valid(): 
            utilisateur = form.cleaned_data['eleve']
            if Adhesion.objects.filter(association=assoce, eleve_id=request.user.profile.id).exists(): #Si l'eleve est membre de l'assoce
                Adhesion.objects.filter(eleve=utilisateur, association=assoce).delete()
            return HttpResponseRedirect('/associations/'+assoce.pseudo)
    else:
        form = AdhesionSuppressionForm(assoce)

    return render(request, 'association/admin.html', {'form': form,})    
@login_required    
#Changer l'ordre des élèves dans le trombi d'une association
def changer_ordre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    nombre_membres = Adhesion.objects.filter(association__pseudo = association_pseudo).count()
    if request.method == 'POST': 
        if Adhesion.objects.filter(association=assoce, eleve_id=request.user.profile.id).exists():#Si l'eleve est membre de l'assoce
            for i in range(1,nombre_membres+1):#Boucle sur les eleves
                adhesion = get_object_or_404(Adhesion,eleve__user__username=request.POST['login-'+str(i)], association = assoce)#On recupert l'eleve par son login
                adhesion.ordre = request.POST['position-'+str(i)]#On change sa position
                adhesion.save()
        return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/') 
    return render(request, 'association/ordre.html', {'association':assoce, 'membres': membres, 'indices_membres': range(nombre_membres)})    
@login_required
def ajouter_affiche(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    if request.method == 'POST':
        formset = AfficheForm(request.POST, request.FILES)
        if Adhesion.objects.filter(association=assoce, eleve_id=request.user.profile.id).exists():# Si l'eleve est membre de l'assoce
            if formset.is_valid():
                affiche = formset.save(commit=False)
                affiche.association = assoce
                affiche.save()
                return HttpResponseRedirect(assoce.get_absolute_url() + 'medias/')
    else:
        formset = AfficheForm()
    return render(request, 'association/ajouter_affiche.html', {'association':assoce, 'membres': membres,   "formset": formset})

@login_required  
def supprimer_affiche(request,association_pseudo,affiche_id):
    affiche = get_object_or_404(Affiche,pk=affiche_id)
    association = affiche.association
    if Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists():# Si l'eleve est membre de l'assoce
        affiche.delete()
    return HttpResponseRedirect(association.get_absolute_url() + 'medias/')


@login_required     
def ajouter_video(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    if request.method == 'POST':
        formset = VideoForm(request.POST, request.FILES)
        if Adhesion.objects.filter(association=assoce, eleve_id=request.user.profile.id).exists():# Si l'eleve est membre de l'assoce
            if formset.is_valid():
                video = formset.save(commit=False)
                video.association = assoce
                video.save()
                return HttpResponseRedirect(assoce.get_absolute_url() + 'medias/')
    else:
        formset = VideoForm()
    return render(request, 'association/ajouter_video.html', {'association':assoce, 'membres': membres,   "formset": formset})

    
@login_required
def supprimer_video(request, association_pseudo, video_id):
    video = get_object_or_404(Video,pk=video_id)
    association = video.association
    if Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists():# Si l'eleve est membre de l'assoce
        video.delete()
    return HttpResponseRedirect(association.get_absolute_url() + 'medias/')


@login_required
def description(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)

    return render(request, 'association/description.html', {'association' : association, 'description' : association.description, 'canEdit' : Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists() })


@login_required
def changeDescription(request, association_pseudo):
    association = get_object_or_404(Association, pseudo=association_pseudo)
    if association.est_cachee_a(request.user.profile):
        return redirect(index)

    if Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists():  # Si l'eleve est membre de l'assoce

        if request.method == 'POST':
            newDescription = request.POST['description']
            association.description = newDescription
            association.save()

        return render(request, 'association/editDescription.html',
                      {'association': association, 'form': DescriptionForm(initial={"description" : association.description}), 'description': association.description})
    else:
        return HttpResponseRedirect(reverse(description, args=[association.nom]))


def getNews(request, association_pseudo):
    association = get_object_or_404(Association, pseudo=association_pseudo)
    if request.user.profile.en_premiere_annee():
        news = News.objects.filter(association=association, hiddenFrom1A=False).order_by("-datePubli")
    else:
        news = News.objects.filter(association=association).order_by("-datePubli")
    return render(request, 'association/news.html',
                  {'association': association, 'news':news,
                   'canEdit': Adhesion.objects.filter(association=association,
                                                      eleve_id=request.user.profile.id).exists()})


class AjouterNews(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'association/form_news.html'

    def form_valid(self, form):
        entree = form.save(commit=False)
        entree.auteur = self.request.user.profile
        entree.association = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])
        entree.save()
        #return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user})
        return HttpResponseRedirect(reverse(getNews, args=[entree.association.pseudo]))


    def dispatch(self, request, *args, **kwargs):
        association = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])
        if not(Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists()):
            raise Http404

        return super(AjouterNews, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        context['mineur'] = self.request.user
        context['association'] = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])
        return context


class ModifierNews(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'association/form_news.html'

    def form_valid(self, form):
        entree = form.save()
        return HttpResponseRedirect(reverse(getNews, args=[entree.association.pseudo]))

    def dispatch(self, request, *args, **kwargs):
        association = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])
        if not (Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists()):
            raise Http404

        return super(ModifierNews, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        context['mineur'] = self.request.user
        context['association'] = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])

        return context

class SupprimerNews(DeleteView):
    model = News
    template_name = 'association/form_news.html'
    success_url = reverse_lazy('associations')

    def dispatch(self, request, *args, **kwargs):
        association = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])
        if not (Adhesion.objects.filter(association=association, eleve_id=request.user.profile.id).exists()):
            raise Http404

        return super(SupprimerNews, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)

        context['mineur'] = self.request.user
        context['association'] = get_object_or_404(Association, pseudo=self.kwargs['association_pseudo'])

        return context

