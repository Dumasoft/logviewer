from django.urls import re_path, path
from .views import LogJsonView, LogViewerView, LogDownloadView, LogRefreshFileView


urlpatterns = [
    re_path(r'^json/(?P<file_name>[\.\w-]*)/(?P<page>[0-9]+)$', LogJsonView.as_view(), name='log_json_view'),
    re_path(r'^json/(?P<file_name>[\.\w-]*)$', LogJsonView.as_view(), name='log_json_view'),
    re_path(r'^delete/(?P<file_name>[\.\w-]*)$', LogRefreshFileView.as_view(), name='refresh_file_log'),
    re_path(r'^download/single-file/(?P<file_name>[\.\w-]*)$', LogDownloadView.as_view(), name='log_download_file_view'),
    path('download.zip/', LogDownloadView.as_view(), name='log_download_zip_view'),
    path('', LogViewerView.as_view(), name='log_file_view'),
]
