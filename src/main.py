import PyPDF2
from io import BytesIO

def main(context):
    headers = {
        'Access-Control-Allow-Origin': '*',  # O reemplaza '*' por tu dominio, ej: 'http://127.0.0.1:5500'
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # Manejar preflight OPTIONS (navegadores envían OPTIONS antes del POST)
    if context.req.method == "OPTIONS":
        return context.res.text("", status_code=204, headers=headers)

    if context.req.method != "POST":
        return context.res.text("Método no permitido, use POST", status_code=405, headers=headers)

    files = context.req.files
    if 'file' not in files:
        return context.res.text("No se encontró archivo 'file' en la petición", status_code=400, headers=headers)

    file = files['file']
    pdf_bytes = BytesIO(file.data)

    try:
        reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return context.res.json({
            "filename": file.filename,
            "text": text[:5000]
        }, headers=headers)
    except Exception as e:
        return context.res.text(f"Error al procesar PDF: {str(e)}", status_code=500, headers=headers)
