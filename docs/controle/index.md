# Controle

**Responsável:** Pietro Ritchele

Área responsável pelo referencial teórico e pela modelagem das funções de controle do braço robótico.

## Atribuições

- Preparar o **referencial teórico** necessário ao funcionamento ideal do robô
- Consolidar o referencial matemático para modelar a **malha PID** de controle
- Modelar as funções de controle em código (em articulação com Software)

## Entregáveis esperados

| Entregável | Descrição | Status |
| ---------- | --------- | ------ |
| Referencial teórico | Bases matemáticas e hipóteses de modelagem | Em definição |
| Modelagem da malha PID | Estrutura, parâmetros e justificativas | Em definição |
| Funções de controle | Especificação para implementação em código | Em definição |

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Referencial teórico](referencial-teorico.md) | Fundamentos e contas da malha de controle |
| [Design de controle](design-de-controle.md) | Projeto da malha PID e funções de controle |

## Observações de escopo

!!! note "Integração com Software"
    As análises de controle devem ser unificadas e prontificadas em código pela área de Software, respeitando:

    - códigos principais enxutos no texto
    - libs, defs e completude fora do texto
    - inputs e outputs bem definidos

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Implementação em código | Software | Funções de controle → repositório |
| Atuadores e realimentação | Eletrônica | PCA9685, sensores e sinais |
| Geometria e limites | Mecânica | Dimensões, batentes e envelope |

## Ferramentas

| Ferramenta | Uso |
| ---------- | --- |
| GitHub | Versionamento do material e artefatos |
| Overleaf | Textos finais em LaTeX da praça |
