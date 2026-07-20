# Mecânica

**Responsável:** Raul

Área responsável pela modelagem estrutural do braço no contexto do **bioV2** e das exigências da **ERC**.

## Atribuições

- Modelar o braço no **Fusion 360**, no ambiente comum do robô **bioV2**
- Considerar aspectos de altura, tamanho e demais restrições do bioV2 e da ERC
- Definir o **material** do braço
- Produzir o **referencial teórico** que justifique o design

## Entregáveis esperados

| Entregável | Descrição | Status |
| ---------- | --------- | ------ |
| Modelo CAD do braço | Fusion 360, compatível com bioV2 | Em definição |
| Design para ERC | Funções e restrições da competição contempladas | Em definição |
| Definição de material | Escolha e justificativa | Em definição |
| Referencial teórico | Fundamentação do design mecânico | Em definição |

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Referencial teórico](referencial-teorico.md) | Justificativa técnica do design |
| [Design mecânico](design-mecanico.md) | CAD Fusion 360, material e montagem |

## Observações de escopo

!!! note "Contexto bioV2 e ERC"
    A modelagem deve considerar o ambiente comum do robô bioV2 (altura, tamanho e afins) e todas as funções necessárias à ERC.

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Envelope e batentes | Controle | Limites para a malha de controle |
| Fixação de eletrônica | Eletrônica | Espaço para Raspberry Pi, PCA9685 e cabeamento |
| Massa / geometria | Software / Controle | Parâmetros para modelo e código |

## Ferramentas

| Ferramenta | Uso |
| ---------- | --- |
| Fusion 360 | Modelagem no ambiente comum bioV2 |
| GitHub | Versionamento de artefatos e revisões |
| Overleaf | Textos finais em LaTeX da praça |
