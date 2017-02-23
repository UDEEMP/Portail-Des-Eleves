from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from abatage.models import Abatage
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def archives(request):
    liste_abatages = Abatage.objects.all()
    return render(request, 'abatage/archives.html', {'liste_abatages': liste_abatages})
@login_required
def archives_json(request):
    liste_abatages = Abatage.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_abatages]))
    return response

def archives_visiteur(request):
    abatage_annuel = Abatage.objects.all()[0]
    liste_abatages = Abatage.objects.exclude(id = abatage_annuel.id)
    return render(request, 'abatage/archives_visiteur.html', {'abatage_annuel':abatage_annuel})