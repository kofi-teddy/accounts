from accountancy.mixins import AuditMixin
from accountancy.models import MultiLedgerTransactions
from django.apps import apps
from django.db import models
from simple_history import register
from django.shortcuts import reverse


class Vat(AuditMixin, models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    rate = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )
    registered = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name} - {self.rate}%"

    def get_absolute_url(self):
        return reverse("vat:vat_detail", kwargs={"pk": self.pk})
    
class ModuleTypes:
    def __iter__(self):
        model = apps.get_model(app_label="nominals",
                               model_name="NominalTransaction")
        all_module_types = model.all_module_types
        for tran_type in all_module_types:
            yield tran_type


class VatTransaction(MultiLedgerTransactions):
    vat_types = [
        ("i", "Input"),
        ("o", "Output")
    ]
    tran_type = models.CharField(max_length=10, choices=ModuleTypes())
    vat_type = models.CharField(max_length=2, choices=vat_types)
    vat_code = models.ForeignKey(Vat, on_delete=models.SET_NULL, null=True)
    vat_rate = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )
    goods = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )
    vat = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['module', 'header', 'line', 'field'], name="vat_unique_batch")
        ]
        permissions = [
            # enquiry perms
            ("view_transactions_enquiry", "Can view transactions"),
        ]

    @classmethod
    def fields_to_update(cls):
        return [
            "ref",
            "period",
            "date",
            "tran_type",
            "vat_type",
            "vat_code",
            "vat_rate",
            "goods",
            "vat"
        ]


    def update_details_from_header(self, header):
        super().update_details_from_header(header)
        self.tran_type = header.type