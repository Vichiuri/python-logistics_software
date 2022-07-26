import os
import traceback
from django.conf import settings
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import render_to_string


class RenderPdf:

    @staticmethod
    def create_pdf(template, context):
        try:
            html_string = render_to_string(template, context)
            css = os.path.join(settings.BASE_DIR, 'tally/static/css/pdf.css')
            html = HTML(string=html_string)
            doc = html.render(stylesheets=[css])
            pdf = doc.write_pdf()
            return HttpResponse(pdf, content_type="application/pdf")
        except:
            return HttpResponse(str(traceback.format_exc()), status=404)
