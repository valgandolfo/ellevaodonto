# 🦷 Projeto Elleva Odontologia - Landing Page & PWA

Este documento serve como guia técnico e funcional para o projeto da **Elleva Odontologia**, facilitando a compreensão da estrutura, tecnologias e processos de alteração futuros.

## 🚀 Visão Geral
O projeto é uma Landing Page desenvolvida em **Django**, focada na conversão de leads (agendamentos) e otimizada para dispositivos móveis através de **PWA (Progressive Web App)**.

- **Domínio:** [ellevadontologia.com.br](https://ellevadontologia.com.br)
- **Hospedagem:** Railway (VPS)
- **Tecnologia Principal:** Django + PWA + Tailwind CSS

---

## 🛠️ Stack Técnica
- **Backend:** Django 6.0+
- **Frontend:** HTML5, Tailwind CSS, Swiper.js
- **Banco de Dados:** SQLite (Desenvolvimento) / Configurado para MySQL ou PostgreSQL em Produção via `DATABASE_URL`.
- **Servidor Web:** Gunicorn
- **Arquivos Estáticos:** WhiteNoise
- **Integração PWA:** `django-pwa`

---

## 📂 Estrutura de Pastas Principal
- `/pro_elleva/`: Configurações globais do projeto Django (`settings.py`, `urls.py`, `wsgi.py`).
- `/app_elleva/`: Lógica da aplicação (Views de agendamento, modelos de dados).
- `/templates/`: Arquivos HTML.
    - `base.html`: Estrutura base (Navbar, Footer, chamadas de scripts/estilos).
    - `home.html`: Conteúdo da Landing Page e formulário de contato.
- `/static/`: Ativos do frontend (Imagens, CSS, JS).
- `manage.py`: Utilitário de comando do Django.
- `Procfile`: Comandos para inicialização no Railway.

---

## 📱 Funcionalidades PWA
O PWA está configurado no `settings.py` e permite que o site seja instalado como um aplicativo no celular.
- **Manifest:** Gerado automaticamente pelo `django-pwa`.
- **Cores:** Tema Terracota (#e73111).
- **Ícones:** Localizados em `/static/logo_elleva.jpg`.

---

## 📝 Como Realizar Alterações

### 1. Alterar Textos ou Estrutura
Edite o arquivo `templates/home.html`. Os estilos utilizam **Tailwind CSS**, permitindo ajustes rápidos de layout diretamente nas classes HTML.

### 2. Alterar Cores ou Variáveis de Estilo
Muitas cores estão definidas como variáveis CSS no topo do `base.html` ou em blocos de estilo. Procure por variáveis como `--agende-botao-fundo`.

### 3. Gerenciar Agendamentos (Leads)
Os agendamentos são salvos no modelo `TbTabelaAtendimento`. Eles podem ser visualizados no Admin do Django:
- Acesse: `ellevadontologia.com.br/admin` (será necessário criar um superusuário se não existir).

### 4. Deploy (Railway)
O deploy é automático via Git. Ao fazer um `push` para o repositório conectado, o Railway executa:
1. `python manage.py migrate` (Atualiza banco de dados)
2. `python manage.py collectstatic` (Organiza arquivos estáticos)
3. Inicia o Gunicorn.

---

## 🛠️ Comandos Úteis (Local)
```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar um superusuário para o Admin
python manage.py createsuperuser

# Aplicar mudanças no banco de dados
python manage.py makemigrations
python manage.py migrate
```

---

## 📌 Observações Importantes
- **Imagens:** As fotos da clínica estão em `/static/imagens/`. Para trocar o carrossel, atualize os arquivos nesta pasta.
- **Segurança:** O projeto usa `python-decouple` para gerenciar chaves secretas e configurações de ambiente no Railway.
