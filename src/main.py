import base64
import json
import PyPDF2
from io import BytesIO

def main(context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    if context.req.method == "OPTIONS":
        return context.res.text("", status_code=204, headers=headers)

    if context.req.method != "POST":
        return context.res.text("Método no permitido, use POST", status_code=405, headers=headers)

    try:
        data = json.loads(context.req.body)
        pdf_bytes = BytesIO(base64.b64decode(data['data']))

        reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return context.res.json({
            "filename": data['filename'],
            "text": text[:5000]
        }, headers=headers)
    except Exception as e:
        return context.res.text(f"Error al procesar PDF: {str(e)}", status_code=500, headers=headers)
