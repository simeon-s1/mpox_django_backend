from django.db.models import F, Count
from rest_framework import serializers, viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from . import models


class ElementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Element
        fields = [
            "id",
            "accession",
            "symbol",
            "description",
            "start",
            "end",
            "strand",
            "sequence",
            "standard",
            "parent",
        ]


class VariantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Variant
        fields = ["id", "label", "ref"]


class ElementReferencesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source="molecule.reference.id")
    accession = serializers.ReadOnlyField(source="molecule.reference.accession")

    class Meta:
        model = models.Element
        fields = ["id", "accession", "sequence"]


class ElementViewSet(viewsets.ModelViewSet):
    queryset = models.Element.objects.all()
    serializer_class = ElementSerializer

    @action(detail=False, methods=["get"])
    def references(self, request: Request, *args, **kwargs):
        queryset = models.Element.objects.filter(type="source")
        serializers = ElementReferencesSerializer(queryset, many=True)
        return Response(serializers.data)

    @action(detail=False, methods=["get"])
    def distinct_genes(self, request: Request, *args, **kwargs):
        queryset = models.Element.objects.distinct("symbol").values("symbol")
        if ref := request.query_params.get("reference"):
            queryset = queryset.filter(molecule__reference__accession=ref)
        return Response({"genes": [item["symbol"] for item in queryset]})


class VariantViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Variant.objects.all()
    serializer_class = VariantSerializer


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sample
        fields = [
            "id",
            "name",
            "sequence",
            "datahash",
        ]


class SampleViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Sample.objects.all()
    serializer_class = SampleSerializer

    @action(detail=False, methods=["get"])
    def count_unique_nt_mut_ref_view_set(self, request: Request, *args, **kwargs):
        # TODO-smc abklären ob das so richtig ist
        queryset = (
            models.Variant.objects.exclude(
                element__type="cds",
                alt="N",
            )
            .values("element__molecule__reference__accession")
            .annotate(count=Count("id"))
        )
        dict = {
            item["element__molecule__reference__accession"]: item["count"]
            for item in queryset
        }
        return Response(data=dict)


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    sequence = serializers.CharField(source="molecules.elements.sequence")

    class Meta:
        model = models.Reference
        fields = ["accession", "description", "organism", "standard", "sequence"]


class ReferenceViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Reference.objects.all()
    serializer_class = ReferenceSerializer


class GenesSerializer(serializers.HyperlinkedModelSerializer):
    reference_accession = serializers.CharField(source="molecule.reference.accession")

    class Meta:
        model = models.Element
        fields = [
            "reference_accession",
            "type",
            "symbol",
            "description",
            "start",
            "end",
            "strand",
            "sequence",
        ]


class GenesViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Element.objects.all()
    serializer_class = GenesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["molecule__reference__accession", "type"]


class SNP1Serializer(serializers.HyperlinkedModelSerializer):
    reference_accession = serializers.CharField(
        source="element.molecule.reference.accession"
    )

    class Meta:
        model = models.Variant
        fields = [
            "reference_accession",
            "ref",
            "alt",
            "start",
            "end",
        ]


class SNP1ViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Variant.objects.filter(
        ref__in=["C", "T", "G", "A"], alt__in=["C", "T", "G", "A"]
    ).exclude(ref=F("alt"))
    serializer_class = SNP1Serializer


class MutationSignatureSerializer(serializers.HyperlinkedModelSerializer):
    reference_accession = serializers.CharField(
        source="element.molecule.reference.accession"
    )
    count = serializers.IntegerField()

    class Meta:
        model = models.Variant
        fields = [
            "reference_accession",
            "ref",
            "alt",
            "start",
            "end",
            "count",
        ]


class MutationSignatureRawSerializer(serializers.HyperlinkedModelSerializer):
    reference_accession = serializers.ReadOnlyField(
        source="element.molecule.reference.accession"
    )

    class Meta:
        model = models.Variant
        fields = [
            "reference_accession",
            "ref",
            "alt",
            "start",
            "end",
        ]


class MutationSignatureViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = (
        models.Variant.objects.filter(ref__in=["C", "T"], alt__in=["C", "T", "G", "A"])
        .exclude(ref=F("alt"))
        .annotate(count=Count("alignments__sequence__samples"))
    )
    serializer_class = MutationSignatureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["element__molecule__reference__accession", "ref", "alt"]

    @action(detail=False, methods=["get"])
    def raw(self, request: Request, *args, **kwargs):
        queryset = models.Variant.objects.filter(
            ref__in=["C", "T"], alt__in=["C", "T", "G", "A"]
        ).exclude(ref=F("alt"))
        page = self.paginate_queryset(queryset)
        serializer = MutationSignatureRawSerializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return self.get_paginated_response(serializer.data)


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    value = serializers.SerializerMethodField()
    name = serializers.ReadOnlyField(source="property.name")

    class Meta:
        model = models.Sample2Property
        fields = [
            "name",
            "value",
        ]

    def get_value(self, obj):
        # get not null field
        return (
            obj.value_integer
            or obj.value_float
            or obj.value_text
            or obj.value_varchar
            or obj.value_blob
            or obj.value_date
            or obj.value_zip
        )


class PropertyViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
    generics.mixins.RetrieveModelMixin,
):
    queryset = models.Sample2Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sample__id", "property__name"]

    @action(detail=False, methods=["get"])
    def unique_collection_dates(self, request: Request, *args, **kwargs):
        queryset = models.Sample2Property.objects.filter(
            property__name="COLLECTION_DATE", value_date__isnull=False
        ).distinct("value_date")
        if ref := request.query_params.get("reference"):
            queryset = queryset.filter(
                sample__sequence__alignment__element__molecule__reference__accession=ref
            )
        queryset = queryset.distinct("value_text")
        date_list = [item.value_date for item in queryset]
        return Response(data={"collection_dates": date_list})

    @action(detail=False, methods=["get"])
    def unique_countries(self, request: Request, *args, **kwargs):
        queryset = models.Sample2Property.objects.filter(
            property__name="COUNTRY", value_text__isnull=False
        )
        if ref := request.query_params.get("reference"):
            queryset = queryset.filter(
                sample__sequence__alignment__element__molecule__reference__accession=ref
            )
        queryset = queryset.distinct("value_text")
        country_list = [item.value_text for item in queryset]
        return Response(data={"countries": country_list})

    @action(detail=False, methods=["get"])
    def unique_sequencing_techs(self, request: Request, *args, **kwargs):
        queryset = models.Sample2Property.objects.filter(
            property__name="SEQ_TECH", value_text__isnull=False
        )
        if ref := request.query_params.get("reference"):
            queryset = queryset.filter(
                sample__sequence__alignment__element__molecule__reference__accession=ref
            )
        queryset = queryset.distinct("value_text")
        sequencing_tech_list = [item.value_text for item in queryset]
        return Response(data={"sequencing_techs": sequencing_tech_list})


class MutationFrequencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Variant
        fields = [
            "element_symbol",
            "variant_label",
            "count",
        ]


class AAMutationViewSet(
    viewsets.GenericViewSet,
    generics.mixins.ListModelMixin,
):
    # input sequencing_tech list, country list, gene list, include partial bool,
    # reference_value int, min_nb_freq int = 1?
    queryset = models.Element.objects.all()

    @action(detail=False, methods=["get"])
    def mutation_frequency(self, request: Request, *args, **kwargs):
        country_list = request.query_params.getlist("countries")
        sequencing_tech_list = request.query_params.getlist("seq_techs")
        gene_list = request.query_params.getlist("genes")
        include_partial = bool(request.query_params.get("include_partial"))
        reference_value = request.query_params.get("reference_value")
        min_nb_freq = request.query_params.get("min_nb_freq")

        samples_query = models.Sample.objects.filter(
            sample2property__property__name="COUNTRY",
            sample2property__value_text__in=country_list,
        ).filter(
            sample2property__property__name="SEQ_TECH",
            sample2property__value_text__in=sequencing_tech_list,
        )
        if not include_partial:
            samples_query.filter(
                sample2property__property__name="GENOME_COMPLETENESS",
                sample2property__value_text="complete",
            )
        variant_query = (
            models.Variant.objects.filter(
                element__molecule__reference__accession=reference_value
            )
            .filter(alignments__sequence__samples__in=samples_query)
            .filter(element__symbol__in=gene_list)
            .annotate(variant_count=Count("alignments__sequence__samples"))
            .filter(variant_count__gte=min_nb_freq)
            .order_by("-variant_count")
        )
        response = [
            {
                "symbol": variant.element.symbol,
                "variant": variant.label,
                "count": variant.variant_count,
            }
            for variant in variant_query
        ]

        return Response(data=response)


# class ChloropethDataSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.Variant
#         fields = [
#             "element_symbol",
#             "variant_label",
#             "count",
#         ]


# class ChloropethData(viewsets.ViewSet):
#     @action(detail=False, methods=["get"])
#     def chloropeth(self, request: Request, *args, **kwargs):
#         country_list = request.query_params.getlist("countries")
#         sequencing_tech_list = request.query_params.getlist("seq_techs")
#         gene_list = request.query_params.getlist("genes")
#         include_partial = bool(request.query_params.get("include_partial"))
#         reference_value = request.query_params.get("reference_value")
#         min_nb_freq = request.query_params.get("min_nb_freq")

#         pass


class SampleGenomesSerializer(serializers.HyperlinkedModelSerializer):
    sample_name = serializers.ReadOnlyField(source="sample.name")

    # 
    nuc_profile = serializers.ReadOnlyField(source="sample.nuc_profile")
    aa_profile = serializers.ReadOnlyField(source="sample.aa_profile")
    imported = serializers.ReadOnlyField(source="sample.imported")
    collection_date = serializers.ReadOnlyField(source="sample.collection_date")
    release_date = serializers.ReadOnlyField(source="sample.release_date")
    isolate = serializers.ReadOnlyField(source="sample.isolate")
    length = serializers.ReadOnlyField(source="sample.length")
    seq_tech = serializers.ReadOnlyField(source="sample.seq_tech")
    country = serializers.ReadOnlyField(source="sample.country")
    geo_location = serializers.ReadOnlyField(source="sample.geo_location")
    host = serializers.ReadOnlyField(source="sample.host")
    genome_completeness = serializers.ReadOnlyField()
    reference_accession = serializers.ReadOnlyField()
    class Meta:
        model = models.Sample
        fields = [
            "id",
            "name",
            "sequence",
            "datahash",
        ]


class SampleGenomeViewSet(viewsets.GenericViewSet, generics.mixins.ListModelMixin):
    queryset = models.Sample.objects.all()

    # 