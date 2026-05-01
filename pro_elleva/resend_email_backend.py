import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class ResendEmailBackend(BaseEmailBackend):
    """
    Backend de e-mail usando o SDK oficial do Resend.
    Requer RESEND_API_KEY configurada nas variáveis de ambiente.
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = getattr(settings, 'RESEND_API_KEY', '')
        if not api_key:
            print("[RESEND] ERRO: RESEND_API_KEY não configurada!")
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY não está configurada.")
            return 0

        resend.api_key = api_key
        num_sent = 0

        for message in email_messages:
            try:
                params: resend.Emails.SendParams = {
                    "from": message.from_email,
                    "to": list(message.to),
                    "subject": message.subject,
                    "text": message.body,
                }

                # Suporte a HTML alternativo
                if hasattr(message, 'alternatives'):
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            params['html'] = content
                            break

                email = resend.Emails.send(params)
                print(f"[RESEND] Enviado com sucesso! ID: {email.get('id', 'N/A')}")
                num_sent += 1

            except Exception as e:
                print(f"[RESEND] ERRO ao enviar: {e}")
                if not self.fail_silently:
                    raise

        return num_sent
