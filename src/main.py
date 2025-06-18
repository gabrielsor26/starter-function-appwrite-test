# main.py

from students import get_students

def main(context):
    if context.req.path == "/students":
        students = get_students()
        return context.res.json({"students": students})
    # Puedes agregar más rutas aquí si lo necesitas

    return context.res.text("Ruta no encontrada", status_code=404)
