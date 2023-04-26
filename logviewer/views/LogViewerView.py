from ..settings import LOG_VIEWER_PAGE_LENGTH, LOG_VIEWER_FILE_LIST_STYLES, LOG_VIEWER_FILE_LIST_TITLE
from ..views.TemplateLoginView import TemplateLoginView


class LogViewerView(TemplateLoginView):
	template_name = 'log_viewer.html'

	def get_context_data(self, filename=None, page=1, **kwargs):
		"""
		Lee y devuelve la información de los archivos log en la administración

		:param filename:  Nombre del archivo de logs
		:param page:
		"""
		context = super(LogViewerView, self).get_context_data(**kwargs)
		context['custom_file_list_title'] = LOG_VIEWER_FILE_LIST_TITLE
		context['custom_style_file'] = LOG_VIEWER_FILE_LIST_STYLES
		context['page_length'] = LOG_VIEWER_PAGE_LENGTH
		context['has_permission'] = self.request.user.is_superuser
		return context
