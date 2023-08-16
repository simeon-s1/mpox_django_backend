from django.contrib import admin
from rest_api.models import Alignment
from rest_api.models import Element
from rest_api.models import Elempart
from rest_api.models import Lineages
from rest_api.models import Molecule
from rest_api.models import Property
from rest_api.models import Reference
from rest_api.models import Sample
from rest_api.models import Sample2Property
from rest_api.models import Sequence
from rest_api.models import Translation
from rest_api.models import Variant


admin.site.register(Alignment)
admin.site.register(Lineages)
admin.site.register(Property)
admin.site.register(Sample)
admin.site.register(Sample2Property)
admin.site.register(Sequence)
admin.site.register(Translation)
admin.site.register(Elempart)
admin.site.register(Element)
admin.site.register(Molecule)
admin.site.register(Reference)
admin.site.register(Variant)