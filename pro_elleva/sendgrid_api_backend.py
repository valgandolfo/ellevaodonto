import json
import urllib.request
import urllib.error
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class SendGridAPIBackend(BaseEmailBackend):
    """
    Backend utilizando a API do RESEND via urllib (sem dependências externas).
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Tenta pegar a chave do settings
        api_key = getattr(settings, 'RESEND_API_KEY', '')
        if not api_key:
            print("ERRO: Chave do Resend (RESEND_API_KEY) não configurada no settings ou .env!")
            return 0
            
        num_sent = 0
        for message in email_messages:
            try:
                url = "https://api.resend.com/emails"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # O Resend espera 'to' como uma lista ou string. 
                # message.to já é uma lista no Django.
                data = {
                    "from": message.from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,
                }
                
                req = urllib.request.Request(
                    url, 
                    data=json.dumps(data).encode('utf-8'), 
                    headers=headers,
                    method='POST'
                )
                
                try:
                    with urllib.request.urlopen(req) as response:
                        # Sucesso
                        num_sent += 1
                except urllib.error.HTTPError as e:
                    error_msg = e.read().decode('utf-8')
                    print(f"ERRO API RESEND ({e.code}): {error_msg}")
                    if not self.fail_silently:
                        raise
                
            except Exception as e:
                print(f"ERRO CRÍTICO NO BACKEND DE E-MAIL: {e}")
                if not self.fail_silently:
                    raise
                    
        return num_sent
