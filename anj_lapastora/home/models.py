from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel
from wagtailmarkdown.fields import MarkdownField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Hierarchy of Pages:
#     HomePage
#         MusingsPage
#               MusingsPostPage
#         TechPage
#               MusingsPostPage
#         AtelierPage
#               PhotoPage
#         AboutPage


class HomePage(Page):
    subpage_types = [
        "home.AboutPage",
        "home.MusingsPage",
        "home.TechPage",
        "home.AtelierPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["sections"] = self.get_children().live()

        recent_posts = sorted(
            list(TechPostPage.objects.live().order_by("-date")[:3])
            + list(MusingsPostPage.objects.live().order_by("-date")[:3]),
            key=lambda post: post.date,
            reverse=True,
        )
        context["recent_posts"] = recent_posts[:3]
        context["recent_photos"] = (
            PhotoPage.objects.live().order_by("-first_published_at")[:4]
        )
        return context


class AboutPage(Page):
    parent_page_types = ["home.HomePage"]


class MusingsPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.MusingsPostPage"]

    def get_posts(self):
        return MusingsPostPage.objects.child_of(self).live().order_by("-date")

    def get_context(self, request):
        context = super().get_context(request)

        posts = self.get_posts()
        paginator = Paginator(posts, 4)  # 4 posts per page

        page = request.GET.get("page")

        try:
            posts_paginated = paginator.page(page)
        except PageNotAnInteger:
            posts_paginated = paginator.page(1)
        except EmptyPage:
            posts_paginated = paginator.page(paginator.num_pages)

        context["posts"] = posts_paginated

        return context


class TechPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.TechPostPage"]

    def get_posts(self):
        return TechPostPage.objects.child_of(self).live().order_by("-date")

    def get_context(self, request):
        context = super().get_context(request)

        posts = self.get_posts()
        paginator = Paginator(posts, 4)  # 4 posts per page

        page = request.GET.get("page")

        try:
            posts_paginated = paginator.page(page)
        except PageNotAnInteger:
            posts_paginated = paginator.page(1)
        except EmptyPage:
            posts_paginated = paginator.page(paginator.num_pages)

        context["posts"] = posts_paginated

        return context


class MusingsPostPage(Page):
    parent_page_types = ["home.MusingsPage"]
    date = models.DateField("Post date")
    body = MarkdownField()
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("main_image"),
    ]


class TechPostPage(Page):
    parent_page_types = ["home.TechPage"]
    date = models.DateField("Post date")
    body = MarkdownField()
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("main_image"),
    ]


class AtelierPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.PhotoPage"]

    def get_context(self, request):
        context = super().get_context(request)

        photos = self.get_children().live().specific()

        paginator = Paginator(photos, 12)  # load 12 at a time
        page_number = request.GET.get("page")

        page_obj = paginator.get_page(page_number)

        context["photos"] = page_obj
        return context


class PhotoPage(Page):
    CATEGORY_CHOICES = [
        ("sea_surf", "sea & surf"),
        ("flora", "flora"),
        ("streets_fiestas", "streets & fiestas"),
        ("golden_hour", "golden hour"),
        ("nature", "nature"),
    ]

    parent_page_types = ["home.AtelierPage"]
    subpage_types = []

    photo = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    caption = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    date_taken = models.DateField(default=timezone.now, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("caption"),
        FieldPanel("description"),
        FieldPanel("date_taken"),
        FieldPanel("category"),
    ]


class AboutPage(Page):
    about_left = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    about_right = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    about_bottom = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("about_left"),
        FieldPanel("about_right"),
        FieldPanel("about_bottom"),
    ]
