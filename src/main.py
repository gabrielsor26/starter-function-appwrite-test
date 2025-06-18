import PyPDF2
from io import BytesIO

def main(context):
    if context.req.method != "POST":
        return context.res.text("Método no permitido, use POST", status_code=405)

    files = context.req.files
    if 'file' not in files:
        return context.res.text("No se encontró archivo 'file' en la petición", status_code=400)

    file = files['file']
    pdf_bytes = BytesIO(file.data)

    try:
        reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return context.res.json({
            "filename": file.filename,
            "text": text[:5000]  # Limitar a 5000 caracteres para evitar respuestas muy largas
        })
    except Exception as e:
        return context.res.text(f"Error al procesar PDF: {str(e)}", status_code=500)
