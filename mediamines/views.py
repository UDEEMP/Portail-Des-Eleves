from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mediamines.models import PhotoUploadForm, Photo, GallerieForm, Gallerie
# Create your views here.

@login_required
def test(request):
    #return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form' : PhotoUploadForm()})
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False) # Permet de récupérer l'objet sans sauver
            instance.save()
            return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': PhotoUploadForm()})
            #return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': PhotoUploadForm()})
        else:
            return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': PhotoUploadForm(), 'errors': form.errors})
    else:
        form = PhotoUploadForm()
        return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': PhotoUploadForm()})

def test2(request):
    if request.method == 'POST':
        form = GallerieForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) # Permet de récupérer l'objet sans sauver
            instance.save()
            return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': GallerieForm()})
            #return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': PhotoUploadForm()})
        else:
            return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': GallerieForm(), 'errors': form.errors})
    else:
        form = GallerieForm()
        return render(request, 'trombi/form_instruments.html', {'mineur': request.user, 'form': GallerieForm()})