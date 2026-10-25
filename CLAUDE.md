# Central de Ajuda Honorarium

## Quem sou eu e o objetivo

Sou Daniel, trabalho no suporte da Honorarium (plataforma que ajuda escritórios
contábeis a precificar honorários e gerar propostas e contratos). Estou
estudando Análise e Desenvolvimento de Sistemas e quero migrar para a área de TI
da empresa. Este projeto é ao mesmo tempo um trabalho (uma central de perguntas
e respostas para os clientes) e meu estudo. Vou apresentá-lo ao meu gestor.

## Como quero que você trabalhe comigo (MUITO IMPORTANTE)

- Responda sempre em português do Brasil.
- Eu quero APRENDER. Explique o porquê de cada mudança antes de fazê-la, em
  linguagem simples.
- Trabalhe em passos pequenos, um de cada vez. Não faça várias etapas de uma vez.
- Antes de editar arquivos, diga o que pretende mudar e espere eu concordar.
- Não faça refatorações grandes nem mude arquivos que eu não pedi.
- Depois de cada mudança, rode os testes (`python manage.py test`) e me diga o
  resultado. Cada funcionalidade nova deve ter teste automático.
- Tudo precisa ser gratuito (sem serviços pagos, sem APIs pagas). Não tenho
  recurso financeiro para isso.
- Uso Mac. Comandos de terminal em formato macOS (python3, source .venv/bin/activate).
- Quando eu terminar um passo, me ajude a conferir no navegador e a entender o
  código que foi escrito.

## Stack

- Python + Django, app principal chamado `faq`
- SQLite (MVP)
- HTML, CSS próprio e Bootstrap 5.3.8 via CDN
- Fontes Google: Poppins (títulos) e Inter (texto)
- Ambiente virtual em `.venv` (ativar com `source .venv/bin/activate`)
- Editor: PyCharm

## Estrutura do projeto

- `config/` configurações do Django (`settings.py`: idioma pt-br, fuso America/Sao_Paulo,
  MEDIA configurado)
- `faq/models.py`
  - `Categoria`: nome (único), descricao, ativa
  - `Artigo`: categoria (ForeignKey com PROTECT, related_name="artigos"), pergunta
    (única), resposta (texto curto), passo_a_passo (uma etapa por linha, numeradas
    "1. ..."), palavras_chave, video (upload), status (fluxo: rascunho,
    em validação, aprovado, publicado), autor, datas de criação e atualização
- `faq/admin.py`: painel da equipe, com ações "Publicar selecionados" e
  "Voltar selecionados para validação", e autor preenchido automaticamente ao criar
- `faq/views.py`: view `inicio` (categorias ativas com contagem de artigos publicados,
  uma única consulta com annotate)
- `faq/templatetags/faq_extras.py`: filtro `separar_etapas`
- `faq/templates/faq/`: `base.html` (cabeçalho, rodapé) e `inicio.html`
- `faq/static/faq/`: `css/style.css` (atual), `css/style-antigo.css` (antigo, só consulta),
  `img/logo.png` (logo PROVISÓRIO recortado de um print; trocar pelo oficial)
- `faq/dados_iniciais.py` e `faq/management/commands/carregar_artigos.py`:
  carga dos 16 artigos iniciais (`python manage.py carregar_artigos [--publicar]`),
  não duplica e não sobrescreve correções feitas pela equipe
- `faq/tests.py`: testes da home, da carga de artigos e do admin
- URL name da home: `inicio`

## Regras de negócio

- O cliente só vê artigos com status publicado e categorias ativas.
- Pergunta duplicada é proibida (unique no banco).
- Categoria com artigos não pode ser excluída (PROTECT).
- Categorias sem artigo publicado não aparecem na home.

## Identidade visual (cores da Honorarium, medidas do site oficial)

Tema escuro, com verde como destaque. Variáveis no `:root` do `style.css`:

- verde da marca `#5dac56` (hover `#6dbd66`), texto sobre verde `#0b0b0d`
- fundo `#0b0b0d`, cartões `#15151b`, campos `#07070a`, bordas `#2a2a2e`
- texto `#ffffff`, texto secundário `#aeb0b3`

Layout inspirado na estrutura da Central de Soluções da Domínio (cabeçalho no topo,
hero com busca, grade de categorias, destaques, página própria por artigo), mas com a
identidade da Honorarium. Nunca copiar logo, textos ou marca de terceiros.

## Onde estamos

Feito:
1. Ajustes de base (idioma, fuso, view eficiente) e testes
2. Carga dos 16 artigos e ação de publicar no admin
3. Nova home: cabeçalho, hero com busca (ainda só visual), grade de categorias
4. Paleta e fontes da Honorarium aplicadas

Próximos passos, nesta ordem:
- Passo 2: página de categoria (lista os artigos da categoria, com paginação) e
  ligar os cartões da home a ela
- Passo 3: página própria de cada artigo (URL única), com resposta, passo a passo
  numerado, vídeo e artigos relacionados
- Passo 4: campo `destaque` no Artigo (migração) e seção Destaques na home
- Passo 5: busca no servidor com página de resultados, ignorando acentos
  (no SQLite, `icontains` não ignora acentos: precisa normalizar). Hoje o campo de
  busca da home ainda não funciona
- Passo 6: testes finais e ajustes para celular
- Depois: Git (`git init`, `.gitignore` com .venv, db.sqlite3, media, .idea),
  converter o vídeo de .mov para .mp4 (hoje o `<source>` usa video/quicktime, que
  falha em alguns navegadores), trocar o logo provisório pelo oficial

Antes de qualquer publicação real: trocar SECRET_KEY, DEBUG=False, definir ALLOWED_HOSTS.

## Cuidados com conteúdo

- Artigos são públicos: nunca colocar senhas, senhas padrão, dados de clientes reais,
  CNPJs ou e-mails reais. Se encontrar algo assim em um artigo, me avise.
- Os artigos foram baseados nos documentos do Painel de Propostas (seções: Dados de
  Envio, Checklist, Itens da Proposta, Pacotes, Serviços adicionais, Serviços
  bonificados, Condições de Pagamento e Condições Gerais). Não invente funcionalidades
  da plataforma que não estejam nesses documentos.
- Falta ainda um artigo sobre como gerar o contrato.
