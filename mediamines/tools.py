#from mediamines.models import get_total_price_for_mediamines_commandes

"""
def get_total_price_for_mediamines_commandes(profile):
    somme = 0
    for commande in DemandeImpression.objects.filter(enAttente = True, userProfile=profile):
        somme += commande.prix
    return somme

def has_enough_money_for_mediamines_commande(profile):
    return profile.solde_mediamines >= profile.get_total_price_for_mediamines_commandes()"""