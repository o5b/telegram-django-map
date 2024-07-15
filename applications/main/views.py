from django.utils.timezone import now
from django.views.generic import DetailView, TemplateView

# from applications.services.models import Popular
from . import models


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slide_list'] = models.Slide.published.all()
        context['index_content'] = models.Index.objects.first()
        # context['popular_list'] = Popular.published.all()
        # context['indexvideo_list'] = models.IndexVideo.published.all().order_by('order')[:6]
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = models.About.objects.first()
        return context


class PageDetailView(DetailView):
    template_name = 'main/page_detail.html'
    model = models.Page
    queryset = model.published.all()
