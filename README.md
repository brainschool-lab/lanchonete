
# Lanchonete API - Estácio ADS

API REST desenvolvida para a disciplina de **Análise e Desenvolvimento de Sistemas (ADS)** na  **Estácio** , focada no gerenciamento de fluxos de uma lanchonete.

---

## Execução do Projeto

Para rodar a API localmente na porta  **8001** , utilize o comando:

**Bash**

```
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

## Marcos de Entrega (Releases)

Este repositório utiliza **Tags Anotadas** para registrar o progresso acadêmico. Cada tag funciona como um "checkpoint" oficial da atividade entregue.

| **Campo**          | **Descrição**                                                    |
| ------------------------ | ------------------------------------------------------------------------ |
| **Formato da Tag** | `AAAA.MM.DD-entrega`(Ex:`2026.05.04-entrega`)                        |
| **Módulo**        | Identifica a funcionalidade trabalhada (ex: Pedidos, Clientes).          |
| **Status**         | Indica se está**Concluído**ou **Parcial (Em progresso)** . |
| **Segurança**     | Garante um ponto de restauração fixo para avaliação do professor.    |

---

## Estrutura do Projeto

A organização segue os princípios de separação de responsabilidades:

| **Diretório** | **Responsabilidade**                                 |
| -------------------- | ---------------------------------------------------------- |
| `api/routes/`      | Definição dos endpoints e rotas do FastAPI.              |
| `domain/`          | Regras de negócio e entidades core do sistema.            |
| `repositories/`    | Camada de persistência de dados (atualmente em memória). |
| `schemas/`         | Modelos de validação e serialização (Pydantic).        |
| `services/`        | Orquestração da lógica entre domínio e repositório.   |
| `tests/`           | Testes automatizados (Unitários e Integração).          |

---

## Tecnologias Utilizadas

| **Tecnologia**  | **Finalidade**                                      |
| --------------------- | --------------------------------------------------------- |
| **Python 3.12** | Linguagem base do projeto.                                |
| **FastAPI**     | Framework web moderno e de alta performance.              |
| **Uvicorn**     | Servidor ASGI para execução da API.                     |
| **Pytest**      | Framework de testes para garantir a qualidade do código. |
