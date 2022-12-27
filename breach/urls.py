from django.urls import path

from .views import (
    BreachHintsView,
    MyBreachesView,
    AllBreachesView,
    BreachDetailView,
    BreachDetailPDFView,
    BreachDeleteView,
    AllBreachDeleteView,
    BreachEditView,
    BreachCreateView,
    BreachCreateDconView,
    BreachCreateBtlView,
    BreachCreateBdescView,
    BreachCreateBaffdView,
    BreachCreateBaffsView,
    BreachCreateBconsView,
    BreachCreateBmeasuresView,
    BreachCreateBcommView,
)

app_name = "breach"

urlpatterns = [
    path("", BreachHintsView.as_view(), name="breach_hints"),
    path("create/", BreachCreateView.as_view(), name="breach_create"),
    path("mybreaches/", MyBreachesView.as_view(), name="my_breaches"),
    path(
        "mybreaches/detail/<slug:slug>/",
        BreachDetailView.as_view(),
        name="breach_detail",
    ),
    path(
        "mybreaches/detail/<slug:slug>/pdf/",
        BreachDetailPDFView.as_view(),
        name="breach_detail_pdf",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/",
        BreachEditView.as_view(),
        name="breach_detail_edit",
    ),
    path(
        "mybreaches/detail/<slug:slug>/delete/",
        BreachDeleteView.as_view(),
        name="breach_detail_delete",
    ),
    path("allbreaches/", AllBreachesView.as_view(), name="all_breaches"),
    path(
        "allbreaches/detail/<slug:slug>/",
        BreachDetailView.as_view(),
        name="all_breach_detail",
    ),
    path(
        "allbreaches/detail/<slug:slug>/pdf/",
        BreachDetailPDFView.as_view(),
        name="all_breach_detail_pdf",
    ),
    path(
        "allbreaches/detail/<slug:slug>/edit/",
        BreachEditView.as_view(),
        name="all_breach_detail_edit",
    ),
    path(
        "allbreaches/detail/<slug:slug>/delete/",
        AllBreachDeleteView.as_view(),
        name="all_breach_detail_delete",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/dcon/",
        BreachCreateDconView.as_view(),
        name="breach_create_dcon",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/btl/",
        BreachCreateBtlView.as_view(),
        name="breach_create_btl",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/bdesc/",
        BreachCreateBdescView.as_view(),
        name="breach_create_bdesc",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/baffd/",
        BreachCreateBaffdView.as_view(),
        name="breach_create_baffd",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/baffs/",
        BreachCreateBaffsView.as_view(),
        name="breach_create_baffs",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/bcons/",
        BreachCreateBconsView.as_view(),
        name="breach_create_bcons",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/bmeasures/",
        BreachCreateBmeasuresView.as_view(),
        name="breach_create_bmeasures",
    ),
    path(
        "mybreaches/detail/<slug:slug>/edit/bcomm/",
        BreachCreateBcommView.as_view(),
        name="breach_create_bcomm",
    ),
]
