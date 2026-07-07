def get_forgot_password_template(
    user_name: str,
    reset_link: str
):
    subject = "Recuperación de contraseña - Study RAG"

    body = f"""
Hola {user_name},

Recibimos una solicitud para restablecer tu contraseña.

Puedes hacerlo desde el siguiente enlace:

{reset_link}

Si no solicitaste este cambio ignora este correo.

Equipo Study RAG
"""

    return subject, body