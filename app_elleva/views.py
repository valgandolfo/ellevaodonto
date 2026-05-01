import re
from urllib.parse import quote
from django.shortcuts import redirect
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

        # Formatar telefone
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
            corpo = f"Nome: {nome}\nTelefone: {telefone_formatado}\nInteresse: {interesse}\nMensagem: {mensagem}"
            try:
                send_mail(
                    assunto,
                    corpo,
                    settings.DEFAULT_FROM_EMAIL,
                    ['contato@ellevaodontologia.com.br'],
                    fail_silently=False,
                )
                print(f"[EMAIL] Enviado com sucesso para contato@ellevaodontologia.com.br")
            except Exception as e:
                print(f"[EMAIL] ERRO: {e}")

            messages.success(request, f"Muito Obrigado {primeiro_nome}! Sua solicitação foi enviada por e-mail e em breve entraremos em contato.")
            return redirect('/#contato')

        else:
            messages.success(request, f"Muito Obrigado {primeiro_nome}! Em breve um membro da nossa equipe entrará em contato.")
            return redirect('/#contato')

    return redirect('/#contato')
