import os
import zipfile
from io import BytesIO

from django.http import HttpResponse, Http404
from django.utils.timezone import now

from ..settings import LOG_VIEWER_FILES_DIR
from ..utils import get_log_files
from ..views.TemplateLoginView import TemplateLoginView


class LogDownloadView(TemplateLoginView):
	def render_to_response(self, context, **response_kwargs):
		file_name = context.get('file_name')
		return self.single_file(file_name) if file_name else self.multiple_files()

	def single_file(self, file_name):
		try:
			uri = os.path.join(LOG_VIEWER_FILES_DIR, file_name)
			with open(uri, mode='rb') as file:
				buffer = file.read()

			response = HttpResponse(buffer, content_type='plain/text')
			response['Content-Disposition'] = f'attachment; filename={file_name}'
			return response
		except FileExistsError as error:
			print(error)
			raise Http404

	def multiple_files(self):
		log_file_result = get_log_files(LOG_VIEWER_FILES_DIR)
		generation_time = now()
		zip_filename = f'log_{generation_time.strftime("%Y%m%dT%H%M%S")}.zip'
		zip_buffer = BytesIO()

		try:
			with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
				for log_dir, log_files in log_file_result.items():
					for log_file in log_files:
						display = os.path.join(log_dir, log_file)
						uri = os.path.join(LOG_VIEWER_FILES_DIR, display)
						with open(uri, 'r') as file:
							zip_file.writestr(f'{display}', file.read())

			zip_buffer.seek(0)
			response = HttpResponse(zip_buffer, content_type='application/zip')
			response['Content-Disposition'] = f'attachment; filename={zip_filename}'
			return response
		except Exception as error:
			print(error)
			raise Http404
