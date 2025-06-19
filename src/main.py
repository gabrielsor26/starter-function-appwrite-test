import base64
import json
import PyPDF2
from io import BytesIO
import traceback

def main(context):
    headers = {
        'Access-Control-Allow-Origin': '*',  # Cambiar por dominio específico en producción
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    # Manejo preflight OPTIONS
    if context.req.method == "OPTIONS":
        print("[DEBUG] Received OPTIONS request")
        return context.res.text("", status_code=204, headers=headers)

    if context.req.method != "POST":
        print(f"[ERROR] Método no permitido: {context.req.method}")
        return context.res.text("Método no permitido, use POST", status_code=405, headers=headers)

    try:
        print("[DEBUG] Cuerpo recibido:", context.req.body)
        data = json.loads(context.req.body)

        if not all(k in data for k in ('filename', 'contentType', 'data')):
            msg = "Faltan campos obligatorios en el JSON: 'filename', 'contentType', 'data'"
            print(f"[ERROR] {msg}")
            return context.res.text(msg, status_code=400, headers=headers)

        pdf_data_b64 = data['data']
        pdf_bytes = BytesIO(base64.b64decode(pdf_data_b64))

        print(f"[DEBUG] Procesando archivo: {data['filename']} ({data['contentType']})")

        reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            print(f"[DEBUG] Página {i+1} texto extraído: {len(page_text)} caracteres")
            text += page_text

        text = text.strip()
        if not text:
            print("[WARN] No se extrajo texto del PDF")

        # Limitar tamaño de texto para evitar respuestas muy grandes
        max_length = 10000
        if len(text) > max_length:
            print(f"[INFO] Texto truncado a {max_length} caracteres")
            text = text[:max_length]

        response = {
            "filename": data['filename'],
            "text": text
        }
        print("[DEBUG] Respuesta preparada con texto extraído")
        return context.res.json(response, headers=headers)

    except json.JSONDecodeError as e:
        error_msg = f"Error al decodificar JSON: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return context.res.text(error_msg, status_code=400, headers=headers)

    except base64.binascii.Error as e:
        error_msg = f"Error al decodificar base64: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return context.res.text(error_msg, status_code=400, headers=headers)

    except PyPDF2.errors.PdfReadError as e:
        error_msg = f"Error al leer PDF: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return context.res.text(error_msg, status_code=400, headers=headers)

    except Exception as e:
        tb = traceback.format_exc()
        print(f"[ERROR] Excepción inesperada: {str(e)}\n{tb}")
        return context.res.text(f"Error interno del servidor: {str(e)}", status_code=500, headers=headers)
