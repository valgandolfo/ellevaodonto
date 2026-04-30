import json
import urllib.request
import urllib.error
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class SendGridAPIBackend(BaseEmailBackend):
    """
    Backend utilizando a API do Resend.com (gratuito e moderno)
    Substituindo o SendGrid que ficou caro.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        api_key = getattr(settings, 'SENDGRID_API_KEY', '') # Vamos manter o nome da variável no settings por enquanto
        if not api_key:
            return 0

        num_sent = 0
        for message in email_messages:
            data = {
                "from": message.from_email if "contato@" in message.from_email else "Elleva <onboarding@resend.dev>",
                "to": message.to,
                "subject": message.subject,
                "text": message.body
            }

            req = urllib.request.Request(
                'https://api.resend.com/emails',
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
            )

            try:
                urllib.request.urlopen(req, timeout=10)
                num_sent += 1
            except Exception as e:
                print(f"Erro no Resend API: {e}")
                if not self.fail_silently:
                    raise
        return num_sent
