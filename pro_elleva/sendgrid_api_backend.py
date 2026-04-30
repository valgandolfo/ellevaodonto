import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class SendGridAPIBackend(BaseEmailBackend):
    """
    Backend utilizando a biblioteca oficial RESEND.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Configura a chave da API
        api_key = getattr(settings, 'SENDGRID_API_KEY', '')
        if not api_key:
            print("ERRO: Chave do Resend não configurada!")
            return 0
            
        resend.api_key = api_key

        num_sent = 0
        for message in email_messages:
            try:
                params = {
                    "from": message.from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,
                }
                
                # Se o domínio não estiver validado, o Resend obriga a usar onboarding@resend.dev
                # Mas como você já validou, o seu e-mail contato@ vai funcionar.
                
                resend.Emails.send(params)
                num_sent += 1
            except Exception as e:
                print(f"ERRO CRÍTICO NO RESEND: {e}")
                if not self.fail_silently:
                    raise
        return num_sent
