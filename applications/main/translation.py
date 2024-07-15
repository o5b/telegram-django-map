from modeltranslation.translator import TranslationOptions, register

from . import models


@register(models.Slide)
class SlideTranslationOptions(TranslationOptions):
    fields = [
        'title',
        'button_text',
        'button_url',
    ]


@register(models.Index)
class IndexTranslationOptions(TranslationOptions):
    fields = [
        'content_1',
        'content_2',
    ]


@register(models.About)
class AboutTranslationOptions(TranslationOptions):
    fields = [
        'content_1',
        # 'comment',
        'content_2',
    ]


@register(models.Preference)
class PreferenceTranslationOptions(TranslationOptions):
    fields = [
        'address',
        'footer_address',
        'map_link',
        'site_title',
        'site_description',
    ]


@register(models.Page)
class PageTranslationOptions(TranslationOptions):
    fields = [
        'title',
        'content',
    ]
