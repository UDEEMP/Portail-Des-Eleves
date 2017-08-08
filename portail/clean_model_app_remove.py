from django.contrib.contenttypes.models import ContentType

# List of deleted apps
DEL_APPS = []
# List of deleted models (that are not in the app deleted) In lowercase!
DEL_MODELS = [

]

ct = ContentType.objects.all().order_by("app_label", "model")

for c in ct:
    if (c.app_label in DEL_APPS) or (c.model in DEL_MODELS):
        print
        "Deleting Content Type %s %s" % (c.app_label, c.model)
        c.delete()