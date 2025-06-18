def get_students():
    return [
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Luis"},
        {"id": 3, "nombre": "María"},
        {"id": 4, "nombre": "Carlos"},
        {"id": 5, "nombre": "Sofía"},
        {"id": 6, "nombre": "Pedro"},
        {"id": 7, "nombre": "Lucía"},
        {"id": 8, "nombre": "Miguel"},
        {"id": 9, "nombre": "Valentina"},
        {"id": 10, "nombre": "Javier"},
    ]

def main(context):
    if context.req.method != "POST":
        return context.res.text("Método no permitido, use POST", status_code=405)
    
    if context.req.path == "/students":
        students = get_students()
        return context.res.json({"students": students})
    
    return context.res.text("Ruta no encontrada", status_code=404)
