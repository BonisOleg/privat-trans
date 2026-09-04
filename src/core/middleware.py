from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

from src.core.i18n import collapse_double_prefix


class CollapseLanguagePrefixMiddleware(MiddlewareMixin):
    def process_request(self, request):
        collapsed = collapse_double_prefix(request.get_full_path())
        if collapsed != request.get_full_path():
            return HttpResponsePermanentRedirect(collapsed)
        return None
