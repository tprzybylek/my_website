from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class AppsIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        apps = self.get_children().live().order_by('-first_published_at')
        context['apps'] = apps
        return context

    parent_page_types = ['home.HomePage']


class AppPage(Page):
    app_name = models.CharField(max_length=125)
    github_url = models.URLField(blank=True)
    app_url = models.URLField(blank=True)
    intro = models.CharField(max_length=250)
    features = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('app_name'),
        MultiFieldPanel([
            FieldPanel('github_url'),
            FieldPanel('app_url'),
        ], heading="App URLs"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('features'),
        ], heading="App description"),
    ]

    parent_page_types = ['portfolio.AppsIndexPage']


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]