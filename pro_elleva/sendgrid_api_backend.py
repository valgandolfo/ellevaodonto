import json
import urllib.request
import urllib.error
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class SendGridAPIBackend(BaseEmailBackend):
    """
    Um backend de e-mail customizado do Django que envia e-mails
    usando a API HTTP v3 do SendGrid, ignorando as portas SMTP bloqueadas.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Lê a chave da API das configurações (settings.py)
        api_key = getattr(settings, 'SENDGRID_API_KEY', '')
        if not api_key:
            print("ERRO: SENDGRID_API_KEY não está configurada no settings.py!")
            return 0

        num_sent = 0
        for message in email_messages:
            data = {
                "personalizations": [
                    {
                        "to": [{"email": to} for to in message.to],
                        "subject": message.subject
                    }
                ],
                "from": {
                    "email": message.from_email,
                    # Se tiver um nome (ex: "Contato Elleva <contato@...>")
                    "name": "Elleva Odontologia"
                },
                "content": [
                    {
                        "type": "text/plain",
                        "value": message.body
                    }
                ]
            }

            # Monta a requisição HTTP POST
            req = urllib.request.Request(
                'https://api.sendgrid.com/v3/mail/send',
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
            )

            try:
                urllib.request.urlopen(req, timeout=10)
                num_sent += 1
            except urllib.error.HTTPError as e:
                # Caso a API recuse (ex: sender não validado, api key errada)
                error_body = e.read().decode('utf-8')
                print(f"SendGrid API HTTPError {e.code}: {error_body}")
                if not self.fail_silently:
                    raise
            except Exception as e:
                print(f"Erro ao conectar com SendGrid API: {e}")
                if not self.fail_silently:
                    raise

        return num_sent
