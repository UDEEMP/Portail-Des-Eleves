from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from mediamines.models import PhotoUploadSingleForm, Photo, GallerieForm, Gallerie, PhotoModifForm
from imagekit import utils as imagekit_utils
# Create your views here.

@login_required
def interfaceAdminMediamine(request):
    return render(request, "mediamines/interface_accueil_mediamine.html", {'galleries': Gallerie.objects.all()})


@login_required
def test(request):
    #return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form' : PhotoUploadForm()})
    if request.method == 'POST':
        form = PhotoUploadSingleForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False) # Permet de récupérer l'objet sans sauver
            instance.save()
            return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form': PhotoUploadSingleForm()})
            #return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form': PhotoUploadForm()})
        else:
            return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form': PhotoUploadSingleForm(), 'errors': form.errors})
    else:
        form = PhotoUploadSingleForm()
        return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form': PhotoUploadSingleForm()})

def test2(request):
    if request.method == 'POST':
        form = GallerieForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) # Permet de récupérer l'objet sans sauver
            instance.save()
            return render(request, 'mediamines/form_gallerie.html', {'mineur': request.user, 'form': GallerieForm()})
            #return render(request, 'mediamines/form_upload_single.html', {'mineur': request.user, 'form': PhotoUploadForm()})
        else:
            return render(request, 'mediamines/form_gallerie.html', {'mineur': request.user, 'form': GallerieForm(), 'errors': form.errors})
    else:
        form = GallerieForm()
        return render(request, 'mediamines/form_gallerie.html', {'mineur': request.user, 'form': GallerieForm()})


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

class ModifierGallerie(UpdateView):
    model = Gallerie
    form_class = GallerieForm
    template_name = 'mediamines/form_gallerie.html'
    success_url = reverse_lazy(interfaceAdminMediamine)
    def form_invalid(self, form):
        return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user, 'form':form})

class SupprimerGallerie(DeleteView):
    model = Gallerie
    template_name = 'mediamines/form_gallerie.html'
    success_url = reverse_lazy(interfaceAdminMediamine)
    def form_invalid(self, form):
        return render(self.request, 'mediamines/form_gallerie.html', {'mineur': self.request.user, 'form':form})


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
        entree.save()
        return HttpResponseRedirect(reverse(interfaceGallerieMediamine, args=[self.kwargs['gallery_id']]))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'mineur': self.request.user, 'form': form})

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

class SupprimerPhoto(DeleteView):
    model = Photo
    template_name = 'mediamines/form_upload_single.html'
    success_url = reverse_lazy(interfaceAdminMediamine)

def cache_clear(request):
    imagekit_utils.get_cache().clear()
    return HttpResponseRedirect(reverse(interfaceAdminMediamine))