from Repositories.ofertas_repo import oferta_repo
from Repositories.delegado_repo import delegado_repo

# ============= FUNCIONES DE VALIDACIÓN =============

def obtener_empresa_oferta(oferta_id):
    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None
    return oferta.get("empresaId")

def obtener_empresa_delegado(usuario_id):
    empresa_id = delegado_repo.obtener_empresa_id_por_usuario(usuario_id)
    return empresa_id

def puede_editar_oferta(tipo_usuario, usuario_id, oferta_id):

    if tipo_usuario == "candidato":
        return False, "Los candidatos no pueden editar ofertas"
    
    # Si es delegado, verificar que sea de la misma empresa
    if tipo_usuario == "delegado":
        empresa_delegado = obtener_empresa_delegado(usuario_id)
        empresa_oferta = obtener_empresa_oferta(oferta_id)
        
        if empresa_delegado != empresa_oferta:
            return False, "Solo puedes editar ofertas de tu empresa"
        
        return True, ""
    
    return False, "Tipo de usuario no válido"

# ============= FUNCIONES PRINCIPALES =============

def obtener_todas():
    ofertas = oferta_repo.obtener_todas()
    if not ofertas:
        return None, "No hay ofertas disponibles", 404
    return ofertas, None, 200

def obtener_ofertas_delegado(usuario_id):
    """Obtiene las ofertas creadas por un delegado (basado en su empresa)"""
    empresa_id = delegado_repo.obtener_empresa_id_por_usuario(usuario_id)
    if not empresa_id:
        return None, "Delegado o empresa no encontrada", 404
    
    ofertas = oferta_repo.obtener_por_empresa(empresa_id)
    if not ofertas:
        return [], None, 200  # Retorna lista vacía si no hay ofertas
    return ofertas, None, 200

def obtener_por_id(oferta_id):
    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404
    return oferta, None, 200

def crear_oferta(usuario_id, titulo, descripcion, profesion):
    if not all([titulo, descripcion, profesion]):
        return None, "Datos no válidos", 400

    empresa_id = delegado_repo.obtener_empresa_id_por_usuario(usuario_id)
    if not empresa_id:
        return None, "Delegado o empresa no encontrada", 404

    oferta_id = oferta_repo.insertar(empresa_id, titulo, descripcion, profesion)
    return oferta_repo.buscar_por_id(oferta_id), None, 201

def actualizar_oferta(oferta_id, titulo, descripcion, profesion, estado):
    if not all([titulo, descripcion, profesion]):
        return None, "Datos no válidos", 400

    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404

    oferta_repo.actualizar(
        oferta_id, titulo, descripcion, profesion,
        estado if estado is not None else oferta["estadoOferta"]
    )
    return oferta_repo.buscar_por_id(oferta_id), None, 200

def eliminar_oferta(oferta_id):
    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404

    oferta_repo.eliminar(oferta_id)
    return oferta, None, 200