from django.urls import path

from .views import (
    RPAHintsView,
    RPACreateView,
    MyRPAsView,
    RPAEditView,
    RPADeleteView,
    AllRPAsView,
    RPADetailView,
    RPADetailPDFView,
    AllRPADeleteView,
    RPACreateRpanmView,
    RPACreateDconView,
    RPACreateJconView,
    RPACreateDpoView,
    RPACreateIrdView,
    RPACreateCpdView,
    RPACreateCpdoView,
    RPACreatePlbView,
    RPACreateDSubView,
    RPACreateTleView,
    RPACreateCrecView,
    RPACreateTtcView,
    RPACreateAgrpView,
    RPACreateTranView,
    RPACreateDproView,
    RPACreatePiaView,
    RPACreateTomView,
    RPACreateAnnexView,
)

app_name = "rpa"

urlpatterns = [
    path("", RPAHintsView.as_view(), name="rpa_hints"),
    path("create/", RPACreateView.as_view(), name="rpa_create"),
    path("myrpas/", MyRPAsView.as_view(), name="my_rpas"),
    path("myrpas/detail/<slug:slug>/", RPADetailView.as_view(), name="rpa_detail"),
    path(
        "myrpas/detail/<slug:slug>/pdf/",
        RPADetailPDFView.as_view(),
        name="rpa_detail_pdf",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/", RPAEditView.as_view(), name="rpa_detail_edit"
    ),
    path(
        "myrpas/detail/<slug:slug>/delete/",
        RPADeleteView.as_view(),
        name="rpa_detail_delete",
    ),
    path("allrpas/", AllRPAsView.as_view(), name="all_rpas"),
    path("allrpas/detail/<slug:slug>/", RPADetailView.as_view(), name="all_rpa_detail"),
    path(
        "allrpas/detail/<slug:slug>/pdf/",
        RPADetailPDFView.as_view(),
        name="all_rpa_detail_pdf",
    ),
    path(
        "allrpas/detail/<slug:slug>/edit/",
        RPAEditView.as_view(),
        name="all_rpa_detail_edit",
    ),
    path(
        "allrpas/detail/<slug:slug>/delete/",
        AllRPADeleteView.as_view(),
        name="all_rpa_detail_delete",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/rpanm/",
        RPACreateRpanmView.as_view(),
        name="rpa_create_rpanm",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/dcon/",
        RPACreateDconView.as_view(),
        name="rpa_create_dcon",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/jcon/",
        RPACreateJconView.as_view(),
        name="rpa_create_jcon",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/dpo/",
        RPACreateDpoView.as_view(),
        name="rpa_create_dpo",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/ird/",
        RPACreateIrdView.as_view(),
        name="rpa_create_ird",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/cpd/",
        RPACreateCpdView.as_view(),
        name="rpa_create_cpd",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/cpdo/",
        RPACreateCpdoView.as_view(),
        name="rpa_create_cpdo",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/plb/",
        RPACreatePlbView.as_view(),
        name="rpa_create_plb",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/dsub/",
        RPACreateDSubView.as_view(),
        {"choice_field": "dsub_cpd_sel"},
        name="rpa_create_dsub",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/tle/",
        RPACreateTleView.as_view(),
        {"choice_field": "tle_cpd_sel"},
        name="rpa_create_tle",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/crec/",
        RPACreateCrecView.as_view(),
        {"choice_field": "crec_cpd_sel"},
        name="rpa_create_crec",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/ttc/",
        RPACreateTtcView.as_view(),
        name="rpa_create_ttc",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/agrp/",
        RPACreateAgrpView.as_view(),
        {"choice_field": "agrp_cpd_sel"},
        name="rpa_create_agrp",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/tran/",
        RPACreateTranView.as_view(),
        name="rpa_create_tran",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/dpro/",
        RPACreateDproView.as_view(),
        name="rpa_create_dpro",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/pia/",
        RPACreatePiaView.as_view(),
        name="rpa_create_pia",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/tom/",
        RPACreateTomView.as_view(),
        name="rpa_create_tom",
    ),
    path(
        "myrpas/detail/<slug:slug>/edit/annex/",
        RPACreateAnnexView.as_view(),
        name="rpa_create_annex",
    ),
]
