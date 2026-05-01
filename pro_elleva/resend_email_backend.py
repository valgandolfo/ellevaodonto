import json
import urllib.request
import urllib.error
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class ResendEmailBackend(BaseEmailBackend):
    """
    Backend de e-mail usando a API do Resend via urllib (sem pacotes externos).
    Requer RESEND_API_KEY no settings/variáveis de ambiente.
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = getattr(settings, 'RESEND_API_KEY', '')
        if not api_key:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY não está configurada.")
            print("ERRO: RESEND_API_KEY não configurada!")
            return 0

        num_sent = 0
        for message in email_messages:
            try:
                url = "https://api.resend.com/emails"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "from": message.from_email,
                    "to": list(message.to),
                    "subject": message.subject,
                    "text": message.body,
                }

                # Suporte a HTML alternativo (caso exista)
                if hasattr(message, 'alternatives'):
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            data['html'] = content
                            break

                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode('utf-8'),
                    headers=headers,
                    method='POST',
                )

                try:
                    with urllib.request.urlopen(req, timeout=15) as response:
                        resp_body = response.read().decode('utf-8')
                        print(f"Resend OK: {resp_body}")
                        num_sent += 1
                except urllib.error.HTTPError as http_err:
                    error_body = http_err.read().decode('utf-8')
                    print(f"ERRO API Resend ({http_err.code}): {error_body}")
                    if not self.fail_silently:
                        raise Exception(f"Resend API error {http_err.code}: {error_body}")

            except Exception as e:
                print(f"ERRO ao enviar e-mail: {e}")
                if not self.fail_silently:
                    raise

        return num_sent
