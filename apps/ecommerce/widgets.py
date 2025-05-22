from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

class NoCurrentFileClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(self.attrs, attrs)
        html = f'<input type="file" name="{name}"'
        for key, val in attrs.items():
            html += f' {key}="{val}"'
        html += '>'
        return mark_safe(html)
