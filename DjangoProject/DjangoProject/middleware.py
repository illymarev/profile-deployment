import sys
from json import dumps
from django.contrib.auth import get_user_model
from urllib.parse import urlparse
from profileapp.models import WebRequest


from django.http import HttpResponsePermanentRedirect

from django.conf import settings
from profileapp import models


class RequestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'hide_post', view_kwargs.pop('hide_post', False))

    def process_response(self, request, response):

        if request.path.endswith('/favicon.ico'):
            return response

        if type(response) == HttpResponsePermanentRedirect and settings.APPEND_SLASH:
            new_location = response.get('location', None)
            content_length = response.get('content-length', None)

            if new_location and content_length == '0':
                new_parsed = urlparse(new_location)

                old = (('http', 'https')[request.is_secure()], request.get_host(), '{0}/'.format(request.path),
                       request.META['QUERY_STRING'])
                new = (new_parsed.scheme, new_parsed.netloc, new_parsed.path, new_parsed.query)

                if old == new:
                    # dont log - it's just adding a /
                    return response
        try:
            self.save(request, response)
        except Exception as e:
            print(sys.stderr, "Error saving request log", e)

        return response

    def save(self, request, response):
        if hasattr(request, 'user'):
            user = request.user if type(request.user) == get_user_model() else None
        else:
            user = None

        meta = request.META.copy()
        meta.pop('QUERY_STRING', None)
        meta.pop('HTTP_COOKIE', None)
        remote_addr_fwd = None

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')

        post = None
        uri = request.build_absolute_uri()
        if request.POST and uri != '/login/':
            post = dumps(request.POST)

        instance = WebRequest(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            uri=request.build_absolute_uri(),
            status_code=response.status_code,
            user_agent=meta.pop('HTTP_USER_AGENT', None),
            remote_addr=meta.pop('REMOTE_ADDR', None),
            remote_addr_fwd=remote_addr_fwd,
            meta=None if not meta else dumps(meta),
            cookies=None if not request.COOKIES else dumps(request.COOKIES),
            get=None if not request.GET else dumps(request.GET),
            post=None if (not request.POST or getattr(request, 'hide_post') == True) else dumps(request.POST),
            raw_post=None if getattr(request, 'hide_post') else request.raw_post_data,
            is_secure=request.is_secure(),
            is_ajax=request.is_ajax(),
            user=user
        )
        instance.save()