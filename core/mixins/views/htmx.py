from abc import abstractmethod, ABC
from typing import Any, Dict, Optional, TypeVar, cast, Generic
from django.db import models
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.db.models import QuerySet

QS = TypeVar('QS', bound=QuerySet[Any])
M = TypeVar("M", bound=models.Model)


class HTMXResponseMixin(ABC, Generic[M]):
    template_name: str
    success_template: Optional[str] = None
    request: HttpRequest

    def form_valid(
            self,
            form: M
    ) -> HttpResponse:
        instance = cast(M, form.save())
        return self.render_htmx_response(instance)

    def form_invalid(
            self,
            form: M
    ) -> HttpResponse:
        html = render_to_string(
            self.template_name,
            self.get_form_invalid_context(form),
            request=self.request
        )
        return HttpResponse(html, status=422)

    @staticmethod
    def get_form_invalid_context(
            form: M
    ) -> Dict[str, Any]:
        return {'form': form}

    @abstractmethod
    def render_htmx_response(
            self,
            instance: models.Model
    ) -> HttpResponse:
        ...


class HTMXDeleteMixin(ABC):
    @abstractmethod
    def get_object(
            self,
            queryset: Optional[QS] = None
    ) -> models.Model:
        ...

    def post(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        self.get_object().delete()
        return HttpResponse('', status=204)
