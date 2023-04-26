import os

from ..mixins import JsonResponseMixin
from ..settings import LOG_VIEWER_FILES_DIR
from ..views.TemplateLoginView import TemplateLoginView


class LogRefreshFileView(JsonResponseMixin, TemplateLoginView):
	def render_to_response(self, context, **response_kwargs):

		# to support Django 3.1.* (fixed issue #6)
		file_name = context.get('file_name')

		if file_name:
			try:
				file_log = os.path.join(LOG_VIEWER_FILES_DIR, file_name)

				with open(file_log, mode='w', encoding='utf8', errors='ignore') as file:
					file.write('')
				context['delete'] = True

			except Exception as error:
				print(error)
				context['delete'] = False

		if 'view' in context:
			del context['view']

		return self.render_to_json_response(context, **response_kwargs)
