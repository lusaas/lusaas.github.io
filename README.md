# GuaipeCare 🐾

## Abrir diretamente no navegador

Abra o arquivo `index.html` na raiz do projeto para acessar a demonstração em HTML e CSS, sem instalar Python ou iniciar um servidor. Os perfis usam os dados de demonstração de `seed.py` e o mesmo arquivo de estilos da aplicação original. As fotos externas do Caramelo precisam de conexão com a internet.

Esta versão estática não consulta o banco de dados nem solicita ou registra localizações. Para usar avistamentos compartilhados, é necessário executar a aplicação Flask descrita abaixo. As URLs estáticas também não substituem automaticamente os endereços NFC `/a/<tag>` da aplicação Flask; uma tag precisa apontar para o endereço público correspondente da versão hospedada.

Para atualizar os arquivos HTML após alterar os dados de demonstração em `seed.py`, execute `python gerar_html.py`. O gerador usa apenas a biblioteca padrão do Python.

> **Coleira inteligente de baixo custo com tag NFC para cães e gatos comunitários.**  
> Ao aproximar o celular da coleira, uma página web é aberta com o perfil completo do animal (saúde, vacinas, cuidadores) e, mediante autorização voluntária de quem escaneou, registra o último local de avistamento.

Projeto desenvolvido no âmbito da disciplina de **Metodologia Científica para Computação** — Universidade Federal de Pelotas (**UFPEL**).  
**Professoras:** Ana Marilza Pernas e Tatiana Aires.

---

## 📌 O Problema

Comunidades urbanas, condomínios e ONGs frequentemente cuidam de animais de rua de forma coletiva. Entretanto, o histórico de saúde, as vacinas aplicadas e a localização desses animais costumam ficar dispersos ou perder-se com o tempo. 

Coleiras convencionais com GPS ativo têm custo elevado, exigem recarga constante de bateria e planos de dados móveis caros. O **GuaipeCare** propõe uma alternativa passiva, sustentável e acessível: uma **tag NFC** na coleira que utiliza o próprio celular das pessoas que encontram o animal para atualizar o histórico.

---

## ⚙️ Como Funciona

```
[ Coleira NFC ] ──(aproximação)──> [ Navegador do Celular ]
                                            │
                                            ├──> GET /a/<tag> (Perfil + Saúde)
                                            │
                                            └──> POST /avistamento/<tag> ──> [ Banco SQLite ]
                                                 (Latitude + Longitude)      (Histórico protegido)
```

1. **Identificação Única:** Cada animal possui uma `tag` segura e não sequencial gravada na tag NFC física da coleira.
2. **Leitura Sem Aplicativo:** Qualquer pessoa com celular com NFC habilitado só precisa aproximar o aparelho da coleira para abrir a página web correspondente (`/a/<tag>`). Não é necessário instalar nenhum aplicativo.
3. **Perfil de Saúde:** A página exibe a foto do animal, espécie, descrição, histórico de vacinas e dados de contato dos cuidadores/ONG responsável.
4. **Avistamento Colaborativo:** O navegador solicita permissão de geolocalização. Se o usuário autorizar, apenas as coordenadas geográficas e o horário são enviados ao backend.

> 📍 **Importante:** A localização não é rastreamento contínuo em tempo real; trata-se de um registro de **último avistamento**, atualizado a cada leitura voluntária da coleira.

---

## 🐶 Animais Pré-Cadastrados na Demonstração

Para facilitar apresentações e testes após clonar o repositório, o banco de dados é inicializado automaticamente com os animais de demonstração:

| Animal | Tag NFC | Descrição | Rota Pública de Demonstração |
|---|---|---|---|
| **Almofadinhas** 🐕 | `almofadinhas` | Cão da integrante Luísa Böhm (com 6 fotos) | `http://localhost:5000/a/almofadinhas` |
| **Caramelo** 🐕 | `QI3u1Kd84hk` | Mascote comunitário do campus da UFPel | `http://localhost:5000/a/QI3u1Kd84hk` |
| **Orelha** 🕊️ | `tsLaXibfAwM` | *Easter egg* / Homenagem comunitária | `http://localhost:5000/a/tsLaXibfAwM` |

*Acessando a raiz (`http://localhost:5000/`), o sistema exibe o menu com as coleiras disponíveis para simular a aproximação NFC.*

---

## 🛡️ Privacidade por Design

- **Consentimento Obrigatório:** A localização só é obtida caso o usuário permita explicitamente no navegador. Caso a permissão seja negada, a página continua funcionando normalmente.
- **Anonimato de quem escaneia:** O sistema **nunca** armazena endereço IP, User-Agent, cookies ou qualquer dado de telemetria de quem realizou a aproximação.
- **Proteção da Localização:** A página pública **nunca exibe coordenadas geográficas**, apenas o horário do último avistamento formatado no fuso horário local (`America/Sao_Paulo`). As coordenadas ficam restritas ao banco de dados e aos cuidadores.
- **Tags Não Sequenciais:** As URLs utilizam códigos aleatórios gerados pelo módulo `secrets`, impedindo varredura de identificadores (enumeração).
- **Chaves Estrangeiras Desacopladas:** Os avistamentos e vacinas referenciam o ID interno do animal; se uma tag física for danificada ou substituída, o histórico de saúde e avistamentos é preservado.

---

## 🖼️ Múltiplas Fotos na Galeria

O GuaipeCare suporta múltiplas imagens por animal sem dependência de bibliotecas externas.
- No campo `foto_url`, informe URLs separadas por vírgula ou quebra de linha (suporta caminhos estáticos locais como `/static/img/foto.jpg` e links externos `https://...`).
- Em telas mobile, as fotos são organizadas automaticamente em uma galeria deslizante com *scroll-snap* nativo.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Descrição |
|---|---|---|
| **Backend** | Python 3.10+ & Flask 3 | API REST leve e renderização server-side |
| **Banco de Dados** | SQLite + Flask-SQLAlchemy | Armazenamento local relacional |
| **Interface** | HTML5 + Jinja2 + CSS puro | Layout *mobile-first*, limpo e responsivo |
| **Geolocalização** | JavaScript puro (Vanilla) | `navigator.geolocation` com envio assíncrono via `fetch` |
| **Hardware** | Tags NFC (NTAG213 / NTAG215) | Tags impermeáveis presas à coleira |

---

## 📁 Estrutura do Projeto

```text
guaipecare/
├── app/
│   ├── __init__.py           # Application Factory e inicialização do banco
│   ├── models.py             # Modelos SQLAlchemy (Animal e Avistamento)
│   ├── routes_public.py      # Rotas públicas (/a/<tag>, POST /avistamento e menu /)
│   ├── routes_admin.py       # Módulo reservado para área administrativa futura
│   ├── templates/
│   │   ├── base.html         # Template base responsivo
│   │   ├── animal.html       # Perfil público do animal e aviso de privacidade
│   │   └── admin/            # Diretório reservado para templates administrativos
│   └── static/
│       ├── css/style.css     # Estilos mobile-first sem frameworks
│       ├── js/geolocalizacao.js # Script nativo de geolocalização e envio
│       └── img/              # Imagens locais (ex: cao-orelha-3.jpg)
├── docs/
│   └── canvas_guaipecare.pdf # Business Model Canvas do projeto
├── config.py                 # Configurações do Flask e SQLite
├── requirements.txt          # Dependências do projeto (gerado via pip freeze)
├── run.py                    # Ponto de entrada da aplicação
├── seed.py                   # Script para sincronizar animais de teste e tags fixas
├── ver_avistamentos.py       # Utilitário CLI para listar avistamentos com link Google Maps
├── README.md                 # Documentação completa
└── .gitignore                # Arquivos ignorados pelo Git
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/guaipeCare.git
cd guaipeCare
```

### 2. Criar e ativar o ambiente virtual
```bash
# No Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# No Windows:
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
flask --app run run --debug
# ou:
python run.py
```

O servidor iniciará em `http://127.0.0.1:5000`.  
*(Na primeira inicialização, os animais de teste e avistamentos iniciais são criados automaticamente caso o banco ainda não exista).*

---

## 📋 Comandos e Scripts Úteis

- **Popular ou restaurar animais de teste:**
  ```bash
  python seed.py
  ```
  Restaura as tags padrão (`QI3u1Kd84hk` e `tsLaXibfAwM`), fotos e dados de contato.

- **Visualizar o histórico de avistamentos:**
  ```bash
  python ver_avistamentos.py
  ```
  Exibe uma tabela no terminal com data local (`America/Sao_Paulo`), nome do animal, coordenadas e link direto para o Google Maps.

---

## 📱 Como Gravar na Tag NFC

1. Instale no celular um aplicativo gravador de NFC (ex: **NFC Tools**, disponível gratuitamente para Android e iOS).
2. Conecte o app local à internet via túnel HTTPS (ex: `ngrok http 5000` ou `cloudflared`) ou use o IP local da sua rede Wi-Fi.
3. No app NFC:
   - Selecione **Escrever** -> **Adicionar um registro** -> **URL / URI**.
   - Insira a URL do animal (ex: `https://meu-dominio.com/a/tsLaXibfAwM`).
   - Aproxime a tag NFC da coleira da traseira do smartphone para gravar.
4. Ao aproximar qualquer smartphone da coleira, a página do animal abrirá imediatamente.

> 💡 **Nota de Desenvolvimento:** A API de Geolocalização dos navegadores requer contexto seguro (`https://`) ou `localhost` para solicitar a permissão do GPS.

---

## 🗺️ Status de Implementação e Trabalhos Futuros

- [x] Página pública responsiva do animal (nome, espécie, vacinas, contato, galeria)
- [x] Rota de coleta de geolocalização com consentimento e validação estrita
- [x] Suporte a múltiplas fotos na galeria (CSS nativo)
- [x] Persistência relacional em SQLite com tratamento de tags seguras
- [x] Dados de demonstração pré-configurados e persistentes
- [x] Utilitário CLI para acompanhamento de avistamentos
- [ ] Painel administrativo para cadastro e edição direta pelos cuidadores *(trabalho futuro)*
- [ ] Sistema de login e autenticação com permissões restritas *(trabalho futuro)*
- [ ] Mapa interativo com histórico de trajetos do animal (Leaflet + OpenStreetMap) *(trabalho futuro)*
- [ ] Fallback com QR Code impresso na própria coleira para aparelhos sem leitor NFC *(trabalho futuro)*

---

## 👥 Equipe do Projeto

- **Lucas Dias**
- **Lúcio Vagner**
- **Luísa Böhm**

*Universidade Federal de Pelotas — UFPEL*
