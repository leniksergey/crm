from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView


class ModelPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def get_permission_required(self):
        if isinstance(self, CreateView):
            action = "add"
        elif isinstance(self, UpdateView):
            action = "change"
        elif isinstance(self, DeleteView):
            action = "delete"
        else:
            action = "view"
        opts = self.model._meta
        return [f"{opts.app_label}.{action}_{opts.model_name}"]