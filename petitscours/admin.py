from petitscours.models import PetitCours 
from django.contrib import admin


class PetitCoursAdmin(admin.ModelAdmin):
    list_display = ('title',  'niveau', 'matiere', 'contact', 'attribue_a', 'date_added', 'date_given', 'visible')
    list_filter = ['date_added', 'visible']
    search_fields = ['title','contact','niveau','matiere']
    list_per_page = 100


admin.site.register(PetitCours,PetitCoursAdmin)
