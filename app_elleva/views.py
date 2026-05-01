import re
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import TbTabelaAtendimento

def agendar_consulta(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        interesse = request.POST.get('interesse')
        mensagem = request.POST.get('mensagem')
        metodo_contato = request.POST.get('metodo_contato')

        # Formatar telefone para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        telefone_numeros = re.sub(r'\D', '', telefone) if telefone else ''
        if len(telefone_numeros) == 11:
            telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
        elif len(telefone_numeros) == 10:
            telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"
        else:
            telefone_formatado = telefone

        TbTabelaAtendimento.objects.create(
            ATE_NOME=nome,
            ATE_TELEFONE=telefone_formatado,
            ATE_INTERESSE=interesse,
            ATE_MENSSAGEM=mensagem
        )

        primeiro_nome = nome.split()[0] if nome else ''

        if metodo_contato == 'whatsapp':
            msg_wa = f"Olá! Me chamo {nome}. Tenho interesse em {interesse}. Minha mensagem: {mensagem}"
            whatsapp_url = f"https://wa.me/5518997304019?text={quote(msg_wa)}"
            return redirect(whatsapp_url)

        elif metodo_contato == 'email':
            assunto = f"Novo Agendamento: {nome} - {interesse}"
            corpo_email = f"Nome: {nome}\nTelefone: {telefone_formatado}\nInteresse: {interesse}\nMensagem: {mensagem}"

            try:
                print(f"[EMAIL] Tentando enviar | FROM: {settings.DEFAULT_FROM_EMAIL} | KEY presente: {bool(settings.RESEND_API_KEY)}")
                send_mail(
                    assunto,
                    corpo_email,
                    settings.DEFAULT_FROM_EMAIL,
                    ['contato@ellevaodontologia.com.br'],
                    fail_silently=False,
                )
                print("[EMAIL] Enviado com sucesso via Resend!")
            except Exception as e:
                print(f"[EMAIL] ERRO AO ENVIAR: {e}")

            mensagem_sucesso = f"Muito Obrigado {primeiro_nome} pelo contato. Sua solicitação foi enviada por e-mail e em breve um membro da nossa equipe entrará em contato."
            messages.success(request, mensagem_sucesso)
            return redirect('/#contato')

        else:
            mensagem_sucesso = f"Muito Obrigado {primeiro_nome} pelo contato. Em breve um membro da nossa equipe entrará em contato para agendar seu atendimento ou tirar suas dúvidas."
            messages.success(request, mensagem_sucesso)
            return redirect('/#contato')

    return redirect('/#contato')


def teste_email(request):
    """View temporária de diagnóstico — acesse /teste-email/ no browser para testar o Resend."""
    import json
    import urllib.request
    import urllib.error
    from django.http import HttpResponse

    api_key = getattr(settings, 'RESEND_API_KEY', '')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'NÃO CONFIGURADO')
    backend = getattr(settings, 'EMAIL_BACKEND', 'NÃO CONFIGURADO')

    linhas = [
        f"EMAIL_BACKEND: {backend}",
        f"DEFAULT_FROM_EMAIL: {from_email}",
        f"RESEND_API_KEY presente: {bool(api_key)}",
        f"RESEND_API_KEY (primeiros 8 chars): {api_key[:8] + '...' if api_key else 'VAZIA'}",
        "---",
        "Tentando enviar e-mail de teste via API do Resend...",
    ]

    if not api_key:
        linhas.append("ERRO: RESEND_API_KEY está vazia! Verifique as variáveis do Railway.")
        return HttpResponse("\n".join(linhas), content_type="text/plain; charset=utf-8")

    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "from": from_email,
            "to": [from_email],
            "subject": "Teste Diagnóstico Elleva",
            "text": "Este é um e-mail de teste enviado pela view de diagnóstico.",
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            resp = response.read().decode('utf-8')
            linhas.append(f"SUCESSO! Resposta do Resend: {resp}")
    except urllib.error.HTTPError as e:
        erro = e.read().decode('utf-8')
        linhas.append(f"ERRO HTTP {e.code}: {erro}")
    except Exception as e:
        linhas.append(f"ERRO GERAL: {e}")

    return HttpResponse("\n".join(linhas), content_type="text/plain; charset=utf-8")

