import os
import re
from itertools import islice

from django.contrib.admin.utils import unquote, quote
from django.utils.functional import SimpleLazyObject

from ..mixins import JsonResponseMixin
from ..settings import LOG_VIEWER_MAX_READ_LINES, LOG_VIEWER_FILES_DIR
from ..utils import get_log_files, readlines_reverse
from ..views.TemplateLoginView import TemplateLoginView


class LogJsonView(JsonResponseMixin, TemplateLoginView):
	def get_log_json(self, original_context=None):
		original_context = {} if original_context is None else original_context

		context = {}
		page = original_context.get('page', 1)
		file_name = original_context.get('file_name', '')

		# Clean the `file_name` to avoid relative paths.
		file_name = unquote(file_name).replace('/..', '').replace('..', '')
		page = int(page)
		current_file = file_name

		lines_per_page = LOG_VIEWER_MAX_READ_LINES
		context['original_file_name'] = file_name
		context['next_page'] = page + 1
		context['log_files'] = []

		log_file_data = get_log_files(LOG_VIEWER_FILES_DIR)
		for log_dir, log_files in log_file_data.items():
			for log_file in log_files:
				display = os.path.join(log_dir, log_file)
				uri = os.path.join(LOG_VIEWER_FILES_DIR, display)

				context['log_files'].append({'name_file': quote(display), 'uri': uri, 'display': display, })

		if file_name:
			try:
				file_log = os.path.join(LOG_VIEWER_FILES_DIR, file_name)

				with open(file_log, encoding='utf8', errors='ignore') as file:
					lines = self.prepare_list_logs(file, page, lines_per_page)
					context['last'] = True if len(lines) < lines_per_page else False
					context['logs'] = self.prepare_list_logs(file, page, lines_per_page)
					context['current_file'] = current_file
					context['file'] = file

			except Exception as error:
				print(error)
				pass
		else:
			context['last'] = True

		if len(context['log_files']) > 0:
			context['log_files'] = sorted(context['log_files'], key=lambda x: sorted(x.items()))
		return context

	def prepare_list_logs(self, file, page, lines_per_page):
		next_lines = list(islice(readlines_reverse(file, exclude='Not Found'),
								 (page - 1) * lines_per_page,
								 page * lines_per_page))
		pattern = re.compile(r'ERROR|INFO|DEBUG|CRITICAL|WARNING')
		lines = pattern.split(next_lines[0])
		lines.pop(0)

		levels = re.findall(r'ERROR|INFO|DEBUG|CRITICAL|WARNING', next_lines[0])
		next_lines = []
		exp = r'\d{4}-\d?\d-\d?\d (?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9],\d{1,6}'

		for index, message in enumerate(lines):
			if index < len(levels):
				date = re.findall(exp, message)[0]
				message = message.replace(f'{date} ', '')
				next_lines.append({'level': levels[index], 'date': date, 'message': message})

		return next_lines

	def render_to_response(self, context, **response_kwargs):

		# to support Django 3.1.* (fixed issue #6)
		file_name = context.get('file_name')
		if isinstance(file_name, SimpleLazyObject):
			context = context['view'].kwargs

		log_json = self.get_log_json(context)

		if 'file' in log_json:
			log_json['file'] = log_json['file'].name

		if 'view' in context:
			del context['view']

		context.update(**log_json)
		return self.render_to_json_response(context, **response_kwargs)
