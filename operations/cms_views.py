"""Generic /ops/cms/ CRUD — one List/Edit/Toggle/Delete implementation
shared by every public-site content model in cms_registry.CMS_REGISTRY,
instead of hand-writing a view+template set per model (mirrors what
CourseListingsView/CourseListingEditView do for a single model)."""

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from .cms_registry import CMS_REGISTRY
from .views import OpsBaseMixin, SuperAdminRequiredMixin


def _entry(model_key):
    entry = CMS_REGISTRY.get(model_key)
    if not entry:
        raise Http404('Unknown content type')
    return entry


class CMSListView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/cms_list.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        model_key = kwargs['model_key']
        entry = _entry(model_key)
        ctx['page_title'] = entry['label']
        ctx['model_key'] = model_key
        ctx['entry'] = entry
        ctx['registry'] = CMS_REGISTRY

        if entry['singleton']:
            instance = entry['model'].load()
            ctx['form'] = ctx.get('form') or entry['form'](instance=instance)
            ctx['instance'] = instance
            return ctx

        qs = entry['model'].objects.all().order_by(*entry['order_fields'])
        section = self.request.GET.get('section', '').strip()
        if section and hasattr(entry['model'], 'section'):
            qs = qs.filter(section=section)
        group = self.request.GET.get('group', '').strip()
        if group and hasattr(entry['model'], 'group'):
            qs = qs.filter(group=group)
        ctx['items'] = qs
        ctx['form'] = ctx.get('form') or entry['form']()
        ctx['selected_section'] = section
        ctx['selected_group'] = group
        return ctx

    def post(self, request, model_key):
        """Singleton models save in place from the list page (no separate add/edit split)."""
        entry = _entry(model_key)
        if not entry['singleton']:
            return redirect('operations:cms_list', model_key=model_key)
        instance = entry['model'].load()
        form = entry['form'](request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('operations:cms_list', model_key=model_key)
        ctx = self.get_context_data(model_key=model_key, form=form)
        ctx['show_errors'] = True
        return self.render_to_response(ctx)


class CMSCreateView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/cms_list.jinja'

    def post(self, request, model_key):
        entry = _entry(model_key)
        if entry['singleton']:
            raise Http404('This content type has a single row — use Edit instead.')
        form = entry['form'](request.POST)
        if form.is_valid():
            form.save()
            return redirect('operations:cms_list', model_key=model_key)
        # Re-render the list with the invalid form + existing items.
        list_view = CMSListView()
        list_view.request = request
        list_view.args = ()
        list_view.kwargs = {'model_key': model_key}
        ctx = list_view.get_context_data(model_key=model_key, form=form)
        ctx['show_errors'] = True
        return self.render_to_response(ctx)


class CMSEditView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/cms_edit.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entry = _entry(kwargs['model_key'])
        instance = get_object_or_404(entry['model'], pk=kwargs['pk'])
        ctx['page_title'] = f"Edit — {entry['label']}"
        ctx['model_key'] = kwargs['model_key']
        ctx['entry'] = entry
        ctx['instance'] = instance
        ctx['form'] = ctx.get('form') or entry['form'](instance=instance)
        return ctx

    def post(self, request, model_key, pk):
        entry = _entry(model_key)
        instance = get_object_or_404(entry['model'], pk=pk)
        form = entry['form'](request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('operations:cms_list', model_key=model_key)
        ctx = self.get_context_data(model_key=model_key, pk=pk, form=form)
        ctx['show_errors'] = True
        return self.render_to_response(ctx)


class CMSToggleView(SuperAdminRequiredMixin, View):
    def post(self, request, model_key, pk):
        entry = _entry(model_key)
        instance = get_object_or_404(entry['model'], pk=pk)
        instance.is_active = not instance.is_active
        instance.save(update_fields=['is_active'])
        return render(request, 'partials/ops/_cms_row.jinja', {
            'item': instance, 'model_key': model_key, 'entry': entry,
        })


class CMSDeleteView(SuperAdminRequiredMixin, View):
    def post(self, request, model_key, pk):
        entry = _entry(model_key)
        entry['model'].objects.filter(pk=pk).delete()
        return HttpResponse('')
