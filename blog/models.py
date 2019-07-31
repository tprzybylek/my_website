from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    # parent_page_types = ['home.HomePage']


class BlogArchivePage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        blogpages = BlogPage.objects.live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    # parent_page_types = ['home.HomePage']


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

    parent_page_types = ['blog.BlogIndexPage']


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]

    parent_page_types = ['blog.BlogIndexPage']


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get('tag')
        if tag:
            blogpages = BlogPage.objects.filter(tags__name=tag)

            context = super().get_context(request)
            context['blogpages'] = blogpages
            return context
        else:
            # TODO: Use taggit tag cloud - https://github.com/feuervogel/django-taggit-templatetags
            tags = Tag.objects.all()

            context = super().get_context(request)
            context['tags'] = tags
            return context

    # parent_page_types = ['home.HomePage']
