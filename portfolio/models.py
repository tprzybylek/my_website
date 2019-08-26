from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

import json


class AppsIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        apps = self.get_children().live().order_by('-first_published_at')
        context['apps'] = apps
        return context

    parent_page_types = ['portfolio.PortfolioHomePage']


class AppPage(Page):
    app_name = models.CharField(max_length=125)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    github_url = models.URLField(blank=True)
    app_url = models.URLField(blank=True)
    presentation_url = models.URLField(blank=True)
    intro = models.CharField(max_length=250)
    features = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('app_name'),

        MultiFieldPanel([
            FieldPanel('github_url'),
            FieldPanel('app_url'),
            FieldPanel('presentation_url'),
        ], heading="App URLs"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('features'),
        ], heading="App description"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
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

    parent_page_types = ['portfolio.PortfolioHomePage']


class PortfolioHomePage(Page):
    parent_page_types = ['wagtailcore.Page']


class ResumePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context['cv'] = json.loads(self.cv)
        return context

    cv = models.TextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('cv'), ]

    parent_page_types = ['portfolio.PortfolioHomePage']
