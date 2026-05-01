import re
import logging
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import TbTabelaAtendimento

logger = logging.getLogger(__name__)

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
                logger.info(f"Tentando enviar e-mail | FROM: {settings.DEFAULT_FROM_EMAIL}")
                send_mail(
                    assunto,
                    corpo_email,
                    settings.DEFAULT_FROM_EMAIL,
                    ['contato@ellevaodontologia.com.br'],
                    fail_silently=False,
                )
                logger.info("E-mail enviado com sucesso via Resend.")
            except Exception as e:
                logger.error(f"ERRO AO ENVIAR E-MAIL: {e}")

            mensagem_sucesso = f"Muito Obrigado {primeiro_nome} pelo contato. Sua solicitação foi enviada por e-mail e em breve um membro da nossa equipe entrará em contato."
            messages.success(request, mensagem_sucesso)
            return redirect('/#contato')

        else:
            mensagem_sucesso = f"Muito Obrigado {primeiro_nome} pelo contato. Em breve um membro da nossa equipe entrará em contato para agendar seu atendimento ou tirar suas dúvidas."
            messages.success(request, mensagem_sucesso)
            return redirect('/#contato')

    return redirect('/#contato')
