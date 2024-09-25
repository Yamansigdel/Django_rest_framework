from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
import os
from django.conf import settings


def save_pdf(params: dict):
    template = get_template("pdf.html")
    html = template.render(params)
  # Create a BytesIO object to hold the PDF
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)  # Convert HTML to PDF

    file_name = str(uuid.uuid4()) # Generate a unique file name
    file_path = os.path.join(settings.MEDIA_ROOT, f'{file_name}.pdf')

    try:
        # Ensure media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        # Write PDF to file
        with open(file_path, 'wb+') as output:
            output.write(response.getvalue())

        print(f"PDF saved at: {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        return '', False

    if pdf.err:
        return '', False

    return file_name, True
