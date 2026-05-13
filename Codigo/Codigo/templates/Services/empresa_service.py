from Repositories.empresa_repo import empresa_repo

def crear_empresa(razon_social, correo_contacto, direccion):
    if not all([razon_social, correo_contacto, direccion]):
        return None, "Datos incompletos", 400

    empresa_id = empresa_repo.crear_empresa(razon_social, correo_contacto, direccion)
    return empresa_repo.buscar_por_id(empresa_id), None, 201

def obtener_empresa(empresa_id):
    empresa = empresa_repo.buscar_por_id(empresa_id)
    if not empresa:
        return None, "Empresa no encontrada", 404
    return empresa, None, 200

def actualizar_empresa(empresa_id, razon_social, correo_contacto, direccion):
    if not all([razon_social, correo_contacto, direccion]):
        return None, "Datos incompletos", 400

    if not empresa_repo.buscar_por_id(empresa_id):
        return None, "Empresa no encontrada", 404

    empresa_repo.actualizar_empresa(empresa_id, razon_social, correo_contacto, direccion)
    return empresa_repo.buscar_por_id(empresa_id), None, 200

def eliminar_empresa(empresa_id):
    empresa = empresa_repo.buscar_por_id(empresa_id)
    if not empresa:
        return None, "Empresa no encontrada", 404

    empresa_repo.eliminar_empresa(empresa_id)
    return empresa, None, 200