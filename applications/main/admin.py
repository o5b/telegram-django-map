from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase
from applications.core.admin import CommonAdmin
from django.contrib import admin
from django.utils.html import mark_safe
from modeltranslation.admin import TabbedTranslationAdmin
from singlemodeladmin import SingleModelAdmin

from . import models


@admin.register(models.Slide)
class SlideAdmin(SortableAdminMixin, CommonAdmin, TabbedTranslationAdmin):
    list_display = ['title', 'thumb_photo', 'status']
    search_fields = ['title']
    readonly_fields = ['thumb_photo']

    def thumb_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="100">')
    thumb_photo.short_description = 'Preview'


@admin.register(models.Index)
class IndexAdmin(SingleModelAdmin, TabbedTranslationAdmin):
    pass


class AboutPhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.AboutPhoto
    readonly_fields = ['thumb_photo']
    extra = 0


@admin.register(models.About)
class AboutAdmin(SortableAdminBase, SingleModelAdmin, TabbedTranslationAdmin):
    inlines = [AboutPhotoInline]


@admin.register(models.Page)
class PageAdmin(CommonAdmin, TabbedTranslationAdmin):
    list_display = ['title', 'get_absolute_url', 'created', 'status']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ['title']}


@admin.register(models.Preference)
class PreferenceAdmin(SingleModelAdmin, TabbedTranslationAdmin):
    pass
