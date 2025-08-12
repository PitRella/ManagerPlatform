from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

QS = TypeVar('QS', bound=QuerySet[Any])
M = TypeVar("M", bound=models.Model)


class HTMXResponseMixin(ABC, Generic[M]):
    """Mixin for handling HTMX-specific form responses.

    This mixin provides functionality for handling form submissions via HTMX,
    including success and error responses. It requires implementation of
     the render_htmx_response method in derived classes.

    Attributes:
        template_name: Template to render for form responses
        success_template: Optional template for successful form submissions
        request: The current HTTP request

    """

    template_name: str
    success_template: str | None = None
    request: HttpRequest

    def form_valid(
            self,
            form: M
    ) -> HttpResponse:
        """Handle valid form submission.

        Args:
            form: The validated form instance

        Returns:
            HttpResponse with rendered template for successful submission

        """
        instance = cast(M, form.save())
        return self.render_htmx_response(instance)

    def form_invalid(
            self,
            form: M
    ) -> HttpResponse:
        """Handle invalid form submission.

        Args:
            form: The invalid form instance

        Returns:
            HttpResponse with rendered template and 422 status code

        """
        html = render_to_string(
            self.template_name,
            self.get_form_invalid_context(form),
            request=self.request
        )
        return HttpResponse(html, status=422)

    @staticmethod
    def get_form_invalid_context(
            form: M
    ) -> dict[str, Any]:
        """Get context data for invalid form rendering.

        Args:
            form: The invalid form instance

        Returns:
            Dict containing form context data

        """
        return {'form': form}

    @abstractmethod
    def render_htmx_response(
            self,
            instance: models.Model
    ) -> HttpResponse:
        """Render HTMX response for successful form submission.

        Args:
            instance: The saved model instance

        Returns:
            HttpResponse with rendered template

        """
        ...


class HTMXDeleteMixin:
    """Mixin for handling HTMX-based delete operations.

    This mixin provides functionality for handling DELETE requests via HTMX,
    allowing for seamless deletion of model instances without page reload.
    The mixin responds with a 204 No Content status code on successful deletion.
    """

    def post(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        """Handle POST request for HTMX-based deletion.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse with 204 status code indicating successful deletion.

        """
        self.get_object().delete()  # type: ignore
        return HttpResponse('', status=204)
