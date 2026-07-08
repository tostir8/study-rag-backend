def get_verify_email_template(
    user_name: str,
    verify_link: str
):
    subject = "Verifica tu correo - Study RAG"

    body = f"""
Hola {user_name},

Gracias por registrarte en Study RAG.

Para verificar tu cuenta da clic en el siguiente enlace:

{verify_link}

Si no realizaste este registro puedes ignorar este correo.

Equipo Study RAG
"""

    return subject, body