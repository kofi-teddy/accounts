from accountancy.views import CashBookAndNominalTransList
from crispy_forms.utils import render_crispy_form
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Sum
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from vat.forms import VatForm, VatTransactionSearchForm
from vat.models import Vat, VatTransaction


class VatTransactionEnquiry(LoginRequiredMixin, CashBookAndNominalTransList):
    model = VatTransaction
    fields = [
        ("module", "Module"),
        ("header", "Internal Ref"),
        ("ref", "Ref"),
        ("period", "Period"),
        ("date", "Date"),
        ("vat_type", "Vat Type"),
        ("goods", "Goods"),
        ("vat", "Vat"),
    ]
    form_field_to_searchable_model_field = {
        "reference": "ref"
    }
    datetime_fields = ["created", "date"]
    datetime_format = '%d %b %Y'
    advanced_search_form_class = VatTransactionSearchForm
    template_name = "vat/transactions.html"
    converters = {
        "vat_type": lambda t : { vat_type[0] : vat_type[1] for vat_type in VatTransaction.vat_types }[t]
    }
    row_identifier = "header"

    def form_valid(self, form):
        queryset = self.apply_advanced_search(form.cleaned_data)
        # ignore voided with it does by default
        return queryset

    def get_transaction_url(self, **kwargs):
        row = kwargs.pop("row")
        module = row.get("module")
        header = row.get("header")
        modules = settings.ACCOUNTANCY_MODULES
        module_name = modules[module]
        return reverse_lazy(module_name + ":view", kwargs={"pk": header})

    def get_queryset(self):
        return (
            VatTransaction.objects
            .all()
            .values(
                *[field[0] for field in self.fields]
            )
            .annotate(Sum("goods"))
            .annotate(Sum("vat"))
            .order_by(*self.order_by())
        )

class LoadVatCodes(LoginRequiredMixin, ListView):
    paginate_by = 50
    model = Vat

    def get_model(self):
        return self.model

    def get_queryset(self):
        if q := self.request.GET.get('q'):
            return (
                self.get_model().objects.annotate(
                    similarity=TrigramSimilarity('code', q),
                ).filter(similarity__gt=0.3).order_by('-similarity')
            )
        return self.get_model().objects.all()

    def render_to_response(self, context, **response_kwargs):
        vats = []
        for vat in context["page_obj"].object_list:
            v = {
                "rate": vat.rate,
                'code': vat.code,
                "id": vat.id
            }
            vats.append(v)
        data = {"data": vats}
        return JsonResponse(data)


class VatList(LoginRequiredMixin, ListView):
    model = Vat
    template_name = "vat/vat_list.html"
    context_object_name = "vats"


class VatDetail(LoginRequiredMixin, DetailView):
    model = Vat
    template_name = "vat/vat_detail.html"


class VatUpdate(LoginRequiredMixin, UpdateView):
    model = Vat
    form_class = VatForm
    template_name = "vat/vat_create_and_edit.html"
    success_url = reverse_lazy("vat:vat_list")
    prefix = "vat"


class VatCreate(LoginRequiredMixin, CreateView):
    model = Vat
    form_class = VatForm
    template_name = "vat/vat_create_and_edit.html"
    success_url = reverse_lazy("vat:vat_list")
    prefix="vat"

    def form_valid(self, form):
        redirect_response = super().form_valid(form)
        if self.request.is_ajax():
            data = {}
            new_vat_code = self.object
            data["new_object"] = {
                "id": new_vat_code.pk,
                "code": str(new_vat_code),
                "rate": new_vat_code.rate
            }
            data["success"] = True
            return JsonResponse(data=data)
        return redirect_response

    def render_to_response(self, context, **response_kwargs):
        # form is not valid
        if self.request.is_ajax():
            ctx = {}
            ctx.update(csrf(self.request))
            form = context["form"]
            form_html = render_crispy_form(form, context=ctx)
            data = {
                "form_html": form_html,
                "success": False
            }
            return JsonResponse(data=data)
        return super().render_to_response(context, **response_kwargs)
