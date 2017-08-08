from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from mediamines.models import *
from imagekit import utils as imagekit_utils
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# Create your views here.

@login_required
@permission_required("mediamines.gestion_photo", raise_exception=True)
def interfaceAdminMediamine(request):
    return render(request, "mediamines/interface_accueil_mediamine.html",
                  {
                      'mineur' : request.user.profile,
                      'galleries': Gallerie.objects.all(),
                      'recaps': RecapitulatifImpressions.objects.filter(isArchived=False, isCanceled=False),
                      'archives': RecapitulatifImpressions.objects.filter(isArchived=True),
                      'annules':RecapitulatifImpressions.objects.filter(isCanceled=True),
                      'demandesEnAttente': DemandeImpression.get_en_attente(),
                      'toutesDemandes': DemandeImpression.objects.all()
                  })



class AjouterGallerie(CreateView):
    model = Gallerie
    form_class = GallerieForm
    template_name = 'mediamines/form_gallerie.html'
    success_url = reverse_lazy(interfaceAdminMediamine)

    def form_valid(self, form):
        entree = form.save(commit=False)
        entree.user_profile = self.request.user.profile
        entree.save()
        #return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user})
        return HttpResponseRedirect(reverse(interfaceAdminMediamine))
    def form_invalid(self, form):
        return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user, 'form':form})


    @method_decorator(permission_required("mediamines.gestion_gallerie", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AjouterGallerie, self).dispatch(request, *args, **kwargs)

class ModifierGallerie(UpdateView):
    model = Gallerie
    form_class = GallerieForm
    template_name = 'mediamines/form_gallerie.html'
    success_url = reverse_lazy(interfaceAdminMediamine)
    def form_invalid(self, form):
        return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user, 'form':form})


    @method_decorator(permission_required("mediamines.gestion_gallerie", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(ModifierGallerie, self).dispatch(request, *args, **kwargs)

class SupprimerGallerie(DeleteView):
    model = Gallerie
    template_name = 'mediamines/form_gallerie.html'
    success_url = reverse_lazy(interfaceAdminMediamine)
    def form_invalid(self, form):
        return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user, 'form':form})


    @method_decorator(permission_required("mediamines.gestion_gallerie", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SupprimerGallerie, self).dispatch(request, *args, **kwargs)

@login_required
@permission_required("mediamines.gestion_gallerie", raise_exception=True)
def interfaceGallerieMediamine(request, gallery_id):
    gallerie = get_object_or_404(Gallerie, pk=gallery_id)
    return render(request, 'mediamines/interface_gallerie_mediamine.html', {'mineur': request.user, 'gallerie': gallerie})

class AjouterPhotoSingle(CreateView):
    model = Photo
    form_class = PhotoUploadSingleForm
    template_name = 'mediamines/form_upload_single.html'
    success_url = reverse_lazy(interfaceGallerieMediamine)

    def form_valid(self, form):
        entree = form.save(commit=False)
        entree.gallerie = get_object_or_404(Gallerie, pk=self.kwargs['gallery_id'])
        entree.uploader = self.request.user.profile
        entree.save()
        return HttpResponseRedirect(reverse(interfaceGallerieMediamine, args=[self.kwargs['gallery_id']]))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'mineur': self.request.user, 'form': form})


    @method_decorator(permission_required("mediamines.gestion_photo", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AjouterPhotoSingle, self).dispatch(request, *args, **kwargs)

class AjouterPhotoMultiple(FormView):
    form_class = PhotoUploadMultiForm
    template_name = 'mediamines/form_upload_multiple.html'
    success_url = reverse_lazy(interfaceGallerieMediamine)

    def form_valid(self, form):
        gallerie = get_object_or_404(Gallerie, pk=self.kwargs['gallery_id'])
        for each in form.cleaned_data['fichiers']:
            Photo.objects.create(gallerie=gallerie, image=each, uploader = self.request.user.profile)
        return HttpResponseRedirect(reverse(interfaceGallerieMediamine, args=[self.kwargs['gallery_id']]))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'mineur': self.request.user, 'form': form})


    @method_decorator(permission_required("mediamines.gestion_photo", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AjouterPhotoMultiple, self).dispatch(request, *args, **kwargs)

class ModifierPhoto(UpdateView):
    model = Photo
    form_class = PhotoModifForm
    template_name = 'mediamines/interface_photo_mediamine.html'
    #success_url = reverse_lazy(interfaceGallerieMediamine)

    def form_valid(self, form):
        entree = form.save()
        #entree.gallerie = get_object_or_404(Gallerie, pk=self.kwargs['gallery_id'])
        #entree.save()
        return HttpResponseRedirect(reverse(interfaceGallerieMediamine, args=[entree.gallerie.id]))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'mineur': self.request.user, 'form': form})

    @method_decorator(permission_required("mediamines.gestion_photo", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(ModifierPhoto, self).dispatch(request, *args, **kwargs)

class SupprimerPhoto(DeleteView):
    model = Photo
    template_name = 'mediamines/form_upload_single.html'
    success_url = reverse_lazy(interfaceAdminMediamine)

    @method_decorator(permission_required("mediamines.gestion_photo", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SupprimerPhoto, self).dispatch(request, *args, **kwargs)

"""def cache_clear(request): # NE MARCHE PAS, get_cache_clear pas fonctionnel ! Remplacé par une suppresion à la main des fichiers du cache, cf models
    imagekit_utils.get_cache().clear()
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))"""

@login_required
def demanderImpression(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    taille = int(request.POST['taille'])
    if taille < 0 or taille >= len(PRIX_PAR_FORMAT):
        return Http404("Contactez l'admin à webmaster-bde@mines-paristech avec le message suivant : <h1>BITE.</h1>")
    if request.method == 'POST':
        DemandeImpression.objects.create(
            userProfile=request.user.profile,
            photo=photo,
            prix=PRIX_PAR_FORMAT[taille],
            taille=taille
        )
        return HttpResponseRedirect(reverse("view_photo_demande", kwargs={'pk': photo_id, 'demande':True}))

    return HttpResponseRedirect(reverse("view_photo", kwargs={'pk': photo_id}))


@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def generateRecapImpression(request):
    RecapitulatifImpressions.generateRecap(request.user.profile)
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))


@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def generateOrDeleteZips(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    recap.generateOrDeleteZips()
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))

@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def debiteOrAnnuleRecap(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    recap.debiteOrAnnule(request.user.profile, not(recap.hasDebited))
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))


@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def cancelRecap(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    recap.cancel(request.user.profile)
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))

@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def changeArchivageRecap(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    recap.archiveOrDesarchive()
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))

@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def detailRecap(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    return render(request, "mediamines/detail_recap.html", {'recap':recap})

"""def download_zip_images(request, recap_id):
    recap = get_object_or_404(RecapitulatifImpressions, pk=recap_id)
    recap.archiveOrDesarchive(request.user.profile)
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))
"""

@login_required
@permission_required("mediamines.gestion_recap", raise_exception=True)
def afficherSoldes(request):
    return render(request, "mediamines/liste_soldes_mediamines.html", {'mineur': request.user, 'liste':UserProfile.objects.exclude(solde_mediamines=0).order_by('-solde_mediamines')})


class modifierSolde(FormView):
    form_class = SoldeModifForm
    template_name = 'mediamines/form_solde_mediamines.html'
    #success_url = reverse_lazy(afficherSoldes)

    @method_decorator(permission_required("mediamines.gestion_recap", raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(modifierSolde, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.cleaned_data['client'].update_solde_mediamines(- form.cleaned_data['credit'])
        HistoriqueActions.objects.create(
            mediamine_user=self.request.user.profile,
            texte="manuel credit "+ form.cleaned_data['credit'].__str__(),
            sommeDebitee=(- form.cleaned_data['credit']).__str__(),
            client= form.cleaned_data['client']
        )
        return afficherSoldes(self.request)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'mineur': self.request.user, 'form': form})


class ClientViewPhoto(UpdateView):
    model = Photo
    form_class = PhotoIdentificationForm
    template_name = 'mediamines/view_photo.html'


    def get_context_data(self, *args, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        context['mineur'] = self.request.user

        photo = get_object_or_404(Photo, pk = self.kwargs['pk'])
        if photo.gallerie.isHiddenFrom1A and self.request.user.profile.en_premiere_annee():
            raise Http404("<h1>Photo inexistante.</h1>")


        context["nextPhoto"] = photo.gallerie.get_next_photo(photo.id)
        context["previousPhoto"] = photo.gallerie.get_previous_photo(photo.id)
        context["photo"] = photo
        context["photos"] = photo.gallerie.get_photos_in_order()
        context["impressionForm"] = PhotoImpressionForm()


        if 'demande' in self.kwargs:
            context["successMsg"] = "Ta demande a été prise en compte !"

        appreciations = AppreciationPhoto.objects.filter(photo=photo)
        nbrOfLikes = appreciations.filter(isLike=True).count()
        nbrOfDislikes = appreciations.filter(isLike=False).count()

        context["nbrOfLikes"] = nbrOfLikes
        context["nbrOfDislikes"] = nbrOfDislikes

        if appreciations.filter(userProfile=self.request.user.profile, isLike=True).count() > 0:
            context["iLikedThis"] = True
        if appreciations.filter(userProfile=self.request.user.profile, isLike=False).count() > 0:
            context["iDislikedThis"] = True

        if self.request.user.is_superuser or self.request.user.has_perm("mediamines.gestion_photo"):
            context["has_right_to_modify"] = True

        return context

    def get_success_url(self):
        return reverse_lazy("view_photo", args=self.args, kwargs=self.kwargs)

@login_required
def client_gallerie_liste(request):
    if request.user.profile.en_premiere_annee():
        return render(request, "mediamines/gallerie_liste.html",
                  {
                      'mineur': request.user.profile,
                      'galleries': Gallerie.objects.exclude(isHiddenFrom1A=True).order_by("-dateFinChrono", "-dateCreation")[:5],
                      "anciennes" : Gallerie.objects.exclude(isHiddenFrom1A=True).order_by("-dateFinChrono", "-dateCreation")[5:]
                  })

    return render(request, "mediamines/gallerie_liste.html",
                  {
                      'mineur': request.user.profile,
                      'galleries': Gallerie.objects.order_by("-dateFinChrono", "-dateCreation")[:5],
                      "anciennes": Gallerie.objects.order_by("-dateFinChrono", "-dateCreation")[5:],
                  })

@login_required
def client_appreciation_photo(request, photo_id, is_like):
    photo = get_object_or_404(Photo, pk=photo_id)

    if(is_like == 'Stop'):
        AppreciationPhoto.objects.filter(userProfile=request.user.profile, photo=photo).delete()
    else:
        is_like = not(is_like == 'False')
        AppreciationPhoto.objects.filter(userProfile=request.user.profile, photo=photo).delete()
        AppreciationPhoto.objects.create(photo=photo, userProfile=request.user.profile, isLike=is_like).save()

    return HttpResponseRedirect(reverse("view_photo", kwargs={'pk':photo_id}))