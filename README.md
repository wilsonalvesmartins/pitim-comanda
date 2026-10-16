# 🍻 Petiscaria Pitim - Cardápio Virtual & Comanda Digital de Mesas

Sistema completo de autoatendimento, comanda digital individual por mesa e painel master para garçons e gerência da **Petiscaria Pitim**.

---

## 🌐 Acesso Rápido

| Ambiente | Link Direto | Descrição |
| :--- | :--- | :--- |
| **Cardápio & Comanda (Cliente)** | [comanda-pitim.187.77.41.37.sslip.io](http://comanda-pitim.187.77.41.37.sslip.io) | Interface mobile-first para o cliente na mesa |
| **Painel Master / Garçons** | [comanda-pitim.187.77.41.37.sslip.io/acesso](http://comanda-pitim.187.77.41.37.sslip.io/acesso) | **Login:** `admin` \| **Senha:** `admin123` |
| **Repositório GitHub** | [wilsonalvesmartins/pitim-comanda](https://github.com/wilsonalvesmartins/pitim-comanda) | Deploy contínuo no Coolify via Docker |

---

## 📋 Visão Geral

O sistema foi desenvolvido para modernizar o atendimento presencial da **Petiscaria Pitim**:
1. O cliente senta à mesa, abre o cardápio no celular, escolhe seus itens e faz o pedido informando **Mesa** e **Nome**.
2. Várias pessoas podem sentar na **mesma mesa** e ter **comandas separadas**, garantindo privacidade no consumo.
3. O histórico puxa uma **janela deslizante de 12 horas** (evita carregar pedidos de dias anteriores e suporta clientes que ficam após a meia-noite).
4. O cliente pode solicitar tanto o fechamento da sua **comanda individual** quanto o **fechamento da mesa inteira**.
5. O **Painel Master** emite **alerta sonoro imediato** (Web Audio API + fallback) e pisca em vermelho na tela a cada novo pedido ou pedido de conta.
6. O garçom pode lançar pedidos verbais manualmente e dar baixa nas comandas ou na mesa completa registrando a forma de pagamento (PIX, Dinheiro, Débito, Crédito).

---

## ✨ Funcionalidades

### 1. Cardápio Virtual (Cliente - `/`)
- **Categorias Oficiais da Casa:**
  - 🍟 **Porções & Petiscos:** Batata simples, batata com cheddar e bacon, polenta frita, mandioca, calabresa acebolada, tilápia crocante, frango a passarinho, tábua de frios, torresmo com mandioca.
  - 🥟 **Bolinhos Artesanais:** Bolinho de costela com mandioca, cabotiá com carne seca, bolinho de queijo, etc.
  - 🍢 **Espetos na Brasa:** Picanha, alcatra, coração de frango, medalhão de frango com bacon, queijo coalho, kafta, romeu e julieta.
  - 🍺 **Cervejas Geladas:** Heineken, Corona, Original, Amstel, Brahma Duplo Malte, Skol.
  - 🥤 **Refrigerantes & Bebidas:** Coca-Cola (Tradicional e Zero), Guaraná Antarctica, Fanta Laranja, Red Bull, Água Mineral com e sem gás, Sucos Del Valle.
- **Busca em Tempo Real:** Filtro instantâneo por nome ou ingrediente.
- **Customização do Item:** Modal para seleção de quantidade e campo de observações (ex: *"bem passada"*, *"sem cebola"*, *"gelo e limão"*).
- **Carrinho Interativo:** Barra inferior flutuante com subtotal e gaveta de confirmação.

### 2. Comanda Digital Individual & Privacidade
- **Identificação Segura:** O cliente informa sua mesa (Mesa 01 a 15, Balcão ou personalizada) e seu nome.
- **Comandas Separadas na Mesma Mesa:** Se João e Maria estiverem na Mesa 04, cada um tem sua própria comanda com seus itens consumidos. Para ver os itens, o sistema exige a combinação exata de Mesa e Nome.
- **Janela Deslizante de 12 Horas:** A consulta ao banco SQLite filtra `created_at >= datetime('now', '-12 hours')`. Isso garante que clientes consumindo de madrugada não tenham comandas quebradas e que mesas do dia anterior não apareçam no turno atual.
- **Acompanhamento de Status:** O cliente vê o status de cada item em tempo real (*Recebido*, *Em preparo*, *Entregue*).

### 3. Opções de Fechamento da Conta
- **"Fechar Minha Comanda":** Solicita a presença do garçom para receber apenas o valor individual daquele cliente.
- **"Fechar Comanda da Mesa Inteira":** Opção para quando um cliente decide pagar a conta da mesa toda ou quando todos na mesa estão indo embora juntos. Notifica a gerência com o total somado de todas as pessoas da mesa.

### 4. Painel Master / Garçons (`/acesso`)
- **Autenticação Segura:** Login protegido via cookie HMAC e token Bearer (`admin` / `admin123`).
- **Alerta Sonoro em Tempo Real:** Conexão contínua via WebSocket (`/ws/admin`) com sintetizador Web Audio API de dois tons (880Hz + 1318Hz) e elemento `<audio>` como fallback para garantir reprodução sonora mesmo com políticas restritivas de navegadores.
- **Banner de Chamadas Urgentes:** Notificação em destaque no topo da tela com efeito pulsante em vermelho quando qualquer cliente solicita fechar a comanda ou a mesa.
- **Grid de Mesas Ativas:**
  - Cartão por mesa com status visual (verde = normal, vermelho pulsante = solicitou conta).
  - Listagem de todas as comandas da mesa, seus respectivos pedidos e valores individuais.
  - Botão **"Adicionar Item"**: Permite ao garçom lançar pedidos verbais diretamente para qualquer mesa e cliente.
  - Botão **"Receber"**: Baixa de comanda individual com escolha do método de pagamento.
  - Botão **"Fechar Mesa"**: Modal que exibe o total acumulado da mesa inteira, lista todas as comandas a quitar e encerra todas de uma vez com o método escolhido.
- **Gestão do Cardápio (CRUD & Preços com 1 Clique):**
  - Edição inline instantânea de preços com salvamento automático.
  - Pausar / Ativar produto (ideal para itens temporariamente esgotados na cozinha).
  - Formulário para adicionar novos itens e bebidas.
- **Relatório de Vendas (Turno de 12h):**
  - Total faturado no turno.
  - Divisão por forma de pagamento (PIX, Dinheiro, Débito, Crédito).
  - Ranking dos itens mais vendidos no turno.

---

## 🏗️ Arquitetura e Tecnologias

```mermaid
flowchart TD
    Client["📱 Cliente (Mesa) /"] -->|HTTP / JSON| API["⚡ FastAPI Backend (Python 3.12)"]
    Admin["💻 Garçom / Master /acesso"] -->|HTTP + WebSocket| API
    API -->|WebSocket Broadcast| Admin
    API -->|Leitura / Escrita (WAL)| DB[("🗄️ SQLite Database (pitim.db)\nVolume Persistente /app/data")]
    Traefik["🌐 Traefik Reverse Proxy (Coolify)"] -->|Roteamento de Porta 8000| API
```

- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic v2, WebSockets.
- **Banco de Dados:** SQLite em modo WAL (`PRAGMA journal_mode=WAL`), índices otimizados para `(table_number, customer_name, created_at)`.
- **Frontend:** SPA responsivo (Mobile-first), Tailwind CSS, FontAwesome 6, Web Audio API.
- **Infraestrutura:** Dockerfile slim, hospedado na VPS via **Coolify** com Traefik e volume persistente montado em `/app/data`.

---

## 📁 Estrutura do Projeto

```text
pitim-comanda/
├── app/
│   ├── __init__.py
│   ├── auth.py             # Autenticação HMAC e controle de sessão admin
│   ├── database.py         # Conexão SQLite, schemas e janelas de 12h
│   ├── main.py             # FastAPI rotas, WebSocket manager e lógica de negócios
│   └── seed_data.py        # Cardápio inicial completo com imagens oficiais
├── static/
│   ├── index.html          # Interface do cliente (Cardápio e Comanda Digital)
│   ├── acesso.html         # Painel Master (Mesas, Garçom, Cardápio, Relatórios)
│   └── uploads/            # Fotos tratadas e logos oficiais da Petiscaria
├── data/                   # Volume persistente montado no Docker (/app/data)
├── Dockerfile              # Imagem Docker otimizada Python 3.12 slim
├── requirements.txt        # Dependências pip
├── test_live.py            # Suite de testes ponta a ponta na API em produção
├── test_close_table.py     # Suite de testes para fechamento de mesas
└── README.md               # Documentação técnica do sistema
```

---

## 📡 Endpoints da API

### Públicos (Cliente)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/products` | Retorna todos os produtos ativos agrupados por categoria |
| `POST` | `/api/orders` | Cria um pedido para uma mesa e nome de cliente |
| `POST` | `/api/comanda/consultar` | Consulta os pedidos e itens consumidos (janela de 12h) |
| `POST` | `/api/comanda/fechar` | Solicita o fechamento de uma comanda individual |
| `POST` | `/api/comanda/fechar-mesa` | Solicita o fechamento da conta de toda a mesa |

### Admin / Master (Protegidos)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Login do administrador (`admin` / `admin123`) |
| `POST` | `/api/auth/logout` | Encerra a sessão |
| `GET` | `/api/admin/active-tables` | Retorna mesas abertas, comandas, totais e notificações |
| `POST` | `/api/admin/manual-order` | Garçom lança itens manualmente para qualquer mesa |
| `POST` | `/api/admin/comanda/{id}/status` | Quita ou altera status de uma comanda individual |
| `POST` | `/api/admin/table/{table_number}/close` | **Fecha e quita todas as comandas da mesa inteira** |
| `POST` | `/api/admin/order-item/{id}/status` | Atualiza status de preparo de um item |
| `POST` | `/api/admin/products` | Cadastra novo produto ou bebida no cardápio |
| `PUT` | `/api/admin/products/{id}` | Edita dados completos do produto |
| `PATCH` | `/api/admin/products/{id}/price` | Edição rápida de preço com 1 clique |
| `PATCH` | `/api/admin/products/{id}/toggle` | Pausa ou ativa o produto |
| `GET` | `/api/admin/reports` | Relatório de vendas e formas de pagamento das últimas 12h |
| `WS` | `/ws/admin` | WebSocket para eventos ao vivo e sinal sonoro |

---

## 💻 Execução Local

### Pré-requisitos
- Python 3.10+ instalado ou Docker.

### Com Python direto:
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Com Docker:
```bash
docker build -t pitim-comanda .
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data --name pitim-app pitim-comanda
```

Acesse:
- **Cardápio:** `http://localhost:8000`
- **Painel Master:** `http://localhost:8000/acesso`

---

## 🚀 Deploy e Infraestrutura (Coolify)

O sistema roda em produção no Coolify:
- **Projeto:** `Pitim Petiscaria`
- **Servidor:** `localhost` (`187.77.41.37`)
- **Porta Interna:** `8000`
- **Volume Persistente:** `pitim-mesas-db-data` montado em `/app/data` (garante que os dados nunca sejam perdidos em novos deploys).
- **Roteamento:** Traefik com suporte a WebSockets nativo.
