# Software

**Responsável:** Felipe das Neves

Área responsável por repositórios, diagramas de software e pela unificação das análises de controle em código.

## Atribuições

- Criar e manter organizados os repositórios utilizados no projeto conceitual
- Unificar as análises de controle e prontificá-las em código
- Modelar os diagramas de **Estados**, **Arquitetura** e **Sequência**

## Entregáveis esperados

| Entregável | Descrição | Status |
| ---------- | --------- | ------ |
| Diagrama de máquina de estados | Comportamento e modos de operação | Em definição |
| Diagrama de arquitetura | Organização dos módulos e interfaces | Em definição |
| Diagrama de sequência | Fluxos principais de interação | Em definição |
| Códigos principais | Python orquestra UI; C controla periféricos | Modelado |

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Diagramas](diagramas.md) | Estados, arquitetura e sequência |
| [Código](codigo.md) | Python (UI) + C (periféricos), IPC JSON |

## Observações de escopo

!!! note "Códigos no texto vs. fora do texto"
    - **Dentro do escopo do texto:** somente os códigos principais, de forma enxuta
    - **Fora do escopo do texto:** códigos em completude, bibliotecas e definições
    - **Inputs e outputs** precisam ficar bem definidos no código

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Funções de controle | Controle | Modelagem da malha → código |
| I/O e drivers | Eletrônica | MCU, PCA9685 e sensores |
| Limites físicos | Mecânica | Envelope e restrições do braço |

## Ferramentas

| Ferramenta | Uso |
| ---------- | --- |
| GitHub | Versionamento e organização dos repositórios |
| Overleaf | Textos finais em LaTeX da praça |
