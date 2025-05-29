# 📚 API de Reserva de Salas

## 🔍 Visão Geral
Este micro serviço tem a responsabilidade de gerenciar as reservas de salas de aula para turmas acadêmicas, conectado ao sistema central de gerenciamento escolar, possibilitando que as instituições educacionais façam reservas de forma eficiente e evitem conflitos de horários.

## 🧩 Arquitetura

A API de Reserva de Salas é um **microsserviço** que faz parte de um sistema maior de [School System](https://github.com/caio-ireno/School-System-Api)
, sendo responsável exclusivamente pelo gerenciamento das reservas de salas por turma.

⚠️ **Esta API depende de outra API de Gerenciamento Escolar (School System)**, que deve estar em execução e exposta localmente. A comunicação entre os serviços ocorre via **requisições HTTP REST**, para validar:


---

## 🚀 Tecnologias Utilizadas

- Python 3.10
- Flask
- SQLite (banco de dados local)
- Docker
- Requests (para consumo da API externa)
- Pytest (para testes)

---

## ▶️ Como Executar a API
### Pré-requisitos:
-Docker instalado
- Sistema de Gerenciamento em execução na porta 5002

### 1. Clone o repositório

```bash
git clone https://github.com/Skyiver/devapisalas.git
```

### 2. Construa e execute o container:

```bash
docker-compose up --build
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a API

```bash
python app.py
```

A aplicação estará disponível em:
📍 `http://localhost:5003`

📝 **Observação:** O banco de dados é criado automaticamente na primeira execução.

---

## 📡 Endpoints Principais

- `GET /api/reservas` – Lista todas as reservas
- `POST /api/reservas` – Cria uma nova reserva de sala
- `GET /api/reservas/<id>` – Obtém uma reserva específica pelo ID
- `POST /api/reseta` – Apaga todas as reservas

### Exemplo de corpo JSON para criação:

```json
{
  "turma_id": 1,
  "sala": "LAB1",
  "data": "2024-12-01",
  "hora_inicio": "09:00",
  "hora_fim": "11:00"
}
```

---

## 🔗 Dependência Externa

Certifique-se de que a **API de Gerenciamento Escolar** esteja rodando em:

```
http://host.docker.internal:5002
```

E que os endpoints de `GET /turmas/<id>` (e opcionalmente `GET /alunos/<id>`) estejam funcionando corretamente para que a validação seja feita com sucesso.

---

##🧪 Como Executar os Testes:

-Testes Unitários:

```bash
docker-compose exec reservas-api pytest tests/test.py -v
```

-Testes de Integração (requer a API de Gestão em execução):

```bash
docker-compose exec reservas-api pytest tests/test_integracao.py -v
```

## 📦 Estrutura do Projeto

```
reserva-salas/
├── app.py                 
├── config.py             
├── docker-compose.yml     
├── Dockerfile             
├── requirements.txt    
│
├── models/                
│   └── reserva.py         
│
├── routes/             
│   └── reserva_route.py 
│
├── services/              
│   └── reserva_service.py 
│
├── tests/               
│   ├── test_integracao.py 
│   └── test.py       
│
└── utils/              
│   └── database.py        
└── README.md
```

---

## 🛠️ Futuras Melhorias

- Desenvolver interface web para visualização das reservas
- Implementar busca de reservas por data/sala
- Implementar autenticação JWT

---

## 🧑‍💻 Autores

* Akira Ogassavara (Curso de SI – Impacta)
* Amanda Costa (Curso de SI – Impacta)
  
