# Rota Compartilhada - Especificação de Requisitos

> Leia este documento com calma. [cite_start]Ele explica o problema que estamos resolvendo, os objetivos do sistema e as regras de negócio que guiam o desenvolvimento[cite: 6, 7, 8].

---

## Introdução

[cite_start]Este documento apresenta a especificação de requisitos do sistema **Rota Compartilhada**, uma aplicação web destinada ao compartilhamento de caronas entre usuários de cidades do sul de Minas Gerais[cite: 8]. [cite_start]Ele descreve o problema identificado, os objetivos, os requisitos funcionais e não funcionais, além das diretrizes técnicas[cite: 9].

O documento está estruturado da seguinte forma:
* [cite_start]**Problema:** A motivação por trás do desenvolvimento[cite: 11].
* [cite_start]**Produto:** Uma visão geral sobre usuários, funcionalidades e limites[cite: 12].
* [cite_start]**Requisitos:** O detalhamento técnico que orientará a construção da aplicação[cite: 13].

---

## Descrição do Problema

[cite_start]Atualmente, muitas pessoas que realizam deslocamentos frequentes entre cidades do sul de Minas enfrentam dificuldades para encontrar caronas[cite: 15]. [cite_start]A organização informal em grupos de redes sociais gera desorganização e falhas na comunicação entre motoristas e passageiros[cite: 16].

**Como isso impacta a vida das pessoas:**
* [cite_start]**Desorganização:** A falta de uma plataforma centralizada gera atrasos e desencontros[cite: 18].
* [cite_start]**Eficiência:** Reduz o aproveitamento dos veículos disponíveis na região[cite: 18].
* [cite_start]**Custo:** Aumenta desnecessariamente os gastos de transporte para os usuários[cite: 19].

[cite_start]Se a tecnologia não melhora a mobilidade e a economia de alguém, não vale a pena construir[cite: 22, 26].

---

## O Produto

| Atributo | Detalhes |
| :--- | :--- |
| **Missão** | [cite_start]Facilitar o compartilhamento de caronas no sul de Minas, promovendo economia e organização[cite: 26]. |
| **Limites** | [cite_start]Aplicação web acessível por navegadores com foco regional inicial[cite: 28, 29]. |
| **Benefícios** | [cite_start]Redução de custos, melhor aproveitamento de veículos e maior comunicação[cite: 31, 32, 35]. |

---

## Lista de Requisitos

### Requisitos Funcionais (RF)

| Nº | Descrição dos Requisitos Funcionais |
| :--- | :--- |
| **RF01** | [cite_start]O sistema deve permitir o cadastro de usuários[cite: 37]. |
| **RF02** | [cite_start]O sistema deve permitir login e autenticação de usuários[cite: 37]. |
| **RF03** | [cite_start]O motorista deve poder cadastrar rotas e horários de viagem[cite: 37]. |
| **RF04** | [cite_start]Passageiros devem poder solicitar uma carona[cite: 37]. |
| **RF05** | [cite_start]Passageiros devem poder buscar caronas disponíveis[cite: 37]. |
| **RF06** | [cite_start]Passageiros devem informar quantas bagagens possuem[cite: 37]. |
| **RF07** | [cite_start]Motoristas devem poder aceitar ou recusar solicitações[cite: 37]. |
| **RF08** | [cite_start]O sistema deve permitir visualizar histórico de viagens[cite: 37]. |

### Requisitos Não Funcionais (RNF)

| Nº | Descrição dos Requisitos Não Funcionais | Detalhamento |
| :--- | :--- | :--- |
| **RNF01** | [cite_start]O sistema deve possuir interface web responsiva[cite: 38]. | [cite_start]Adaptação para diferentes tamanhos de tela[cite: 38]. |
| **RNF02** | [cite_start]Segurança de autenticação dos usuários[cite: 38]. | [cite_start]Garantir acesso restrito e seguro[cite: 38]. |
| **RNF03** | [cite_start]Tempo de resposta adequado[cite: 38]. | [cite_start]O sistema deve responder às requisições com agilidade[cite: 38]. |
| **RNF04** | [cite_start]Disponibilidade mínima[cite: 38]. | [cite_start]Estabilidade durante o uso da plataforma[cite: 38]. |
| **RNF05** | [cite_start]Armazenamento seguro de dados[cite: 38]. | [cite_start]Proteção integral das informações sensíveis[cite: 38]. |

---
[cite_start]**Autor:** Igor de Oliveira Pereira [cite: 3]  
[cite_start]**Muzambinho/MG, 14 de março de 2026** [cite: 4, 5]