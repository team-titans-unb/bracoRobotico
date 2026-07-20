# Eletrônica

**Responsáveis:** João Canabarro e João Gabryel

Área responsável pelos esquemáticos eletrônicos, seleção de componentes e integração elétrica do braço.

## Atribuições

- Modelar os **esquemáticos eletrônicos**
- Definir e documentar os **componentes** que serão utilizados

## Entregáveis esperados

| Entregável | Descrição | Status |
| ---------- | --------- | ------ |
| Diagrama eletrônico completo | Modelado no **Altium** | Em definição |
| Lista de componentes | MCU, drivers, sensores e periféricos | Em definição |
| Interfaces elétricas | Pinagem, barramentos e alimentação | Em definição |

## Componentes de referência (alinhamento inicial)

| Componente | Função | Observação |
| ---------- | ------ | ---------- |
| Raspberry Pi 3 | MCU / computador de bordo principal | Definido no alinhamento |
| PCA9685PW | Driver PWM via I²C | Definido no alinhamento |

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Diagramas](diagramas.md) | Esquemáticos Altium, blocos e pinagem |

## Observações de escopo

!!! danger "Segurança elétrica"
    Antes de ensaios, documente tensões, correntes máximas e o procedimento de energização.

!!! note "Integração com Software e Controle"
    Inputs/outputs e interfaces com a MCU devem ficar explícitos para facilitar a implementação em código.

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Barramentos e I/O | Software | I²C (PCA9685), pinagem e drivers |
| Realimentação | Controle | Sinais para a malha PID |
| Fixação e clearance | Mecânica | Espaço físico de placas e conectores |

## Ferramentas

| Ferramenta | Uso |
| ---------- | --- |
| Altium | Diagrama eletrônico completo |
| GitHub | Versionamento de artefatos |
| Overleaf | Textos finais em LaTeX da praça |
