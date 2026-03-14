# Rota Compartilhada - Especificação de Requisitos

---

## Introdução

Este documento apresenta a especificação de requisitos do sistema **Rota Compartilhada**, uma aplicação web destinada ao compartilhamento de caronas entre usuários de cidades do sul de Minas Gerais. Ele descreve o problema identificado, os objetivos, os requisitos funcionais e não funcionais, além das diretrizes técnicas.

O documento está estruturado da seguinte forma:
* **Problema:** A motivação por trás do desenvolvimento.
* **Produto:** Uma visão geral sobre usuários, funcionalidades e limites.
* **Requisitos:** O detalhamento técnico que orientará a construção da aplicação.

---

## Descrição do Problema

Atualmente, muitas pessoas que realizam deslocamentos frequentes entre cidades do sul de Minas enfrentam dificuldades para encontrar caronas. A organização informal em grupos de redes sociais gera desorganização e falhas na comunicação entre motoristas e passageiros.

**Como isso impacta a vida das pessoas:**
* **Desorganização:** A falta de uma plataforma centralizada gera atrasos e desencontros.
* **Eficiência:** Reduz o aproveitamento dos veículos disponíveis na região.
* **Custo:** Aumenta desnecessariamente os gastos de transporte para os usuários.

Se a tecnologia não melhora a mobilidade e a economia de alguém, não vale a pena construir.

---

## O Produto

| Atributo | Detalhes |
| :--- | :--- |
| **Missão** | Facilitar o compartilhamento de caronas no sul de Minas, promovendo economia e organização. |
| **Limites** | Aplicação web acessível por navegadores com foco regional inicial. |
| **Benefícios** | Redução de custos, melhor aproveitamento de veículos e maior comunicação. |

---

## Lista de Requisitos

### Requisitos Funcionais (RF)

| Nº | Descrição dos Requisitos Funcionais |
| :--- | :--- |
| **RF01** | O sistema deve permitir o cadastro de usuários. |
| **RF02** | O sistema deve permitir login e autenticação de usuários. |
| **RF03** | O motorista deve poder cadastrar rotas e horários de viagem. |
| **RF04** | Passageiros devem poder solicitar uma carona. |
| **RF05** | Passageiros devem poder buscar caronas disponíveis. |
| **RF06** | Passageiros devem informar quantas bagagens possuem. |
| **RF07** | Motoristas devem poder aceitar ou recusar solicitações. |
| **RF08** | O sistema deve permitir visualizar histórico de viagens. |

### Requisitos Não Funcionais (RNF)

| Nº | Descrição dos Requisitos Não Funcionais | Detalhamento |
| :--- | :--- | :--- |
| **RNF01** | O sistema deve possuir interface web responsiva. | Adaptação para diferentes tamanhos de tela. |
| **RNF02** | Segurança de autenticação dos usuários. | Garantir acesso restrito e seguro. |
| **RNF03** | Tempo de resposta adequado. | O sistema deve responder às requisições com agilidade. |
| **RNF04** | Disponibilidade mínima. | Estabilidade durante o uso da plataforma. |
| **RNF05** | Armazenamento seguro de dados. | Proteção integral das informações sensíveis. |

---
**Autor:** Igor de Oliveira Pereira  
**Muzambinho/MG, 14 de março de 2026**