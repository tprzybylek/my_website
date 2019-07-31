from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class AppsIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        apps = self.get_children().live().order_by('-first_published_at')
        context['apps'] = apps
        return context

    # parent_page_types = ['home.HomePage']


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

    # parent_page_types = ['home.HomePage']


class PortfolioHomePage(Page):
    pass


class Education(models.Model):
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    university = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    field_of_study = models.CharField(max_length=64, blank=True, null=True)
    specialization = models.CharField(max_length=64, blank=True, null=True)
    grade = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Experience(models.Model):
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Skill(models.Model):
    category = models.CharField(max_length=64)
    name = models.CharField(max_length=64)


class Language(models.Model):
    language = models.CharField(max_length=64)
    level = models.CharField(max_length=16)


class Resume(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=64, blank=True, null=True)
    resume_title = models.CharField(max_length=64, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.ForeignKey(Experience, on_delete=models.SET_NULL, null=True, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)


class ResumePage(Page):
    parent_page_types = ['home.HomePage']
