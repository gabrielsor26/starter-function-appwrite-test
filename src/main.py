
from src.students import get_students

def main(context):
    # Verificar que el método HTTP sea POST
    if context.req.method != "POST":
        return context.res.text("Método no permitido, use POST", status_code=405)

    # Verificar que la ruta sea /students (opcional, si usas rutas)
    if context.req.path == "/students":
        students = get_students()
        return context.res.json({"students": students})

    # Si la ruta no coincide
    return context.res.text("Ruta no encontrada", status_code=404)
