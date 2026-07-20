# Software

Área responsável pela arquitetura de software, firmwares embarcados, interfaces de operação e integração com as demais disciplinas do braço robótico.

## Escopo

- Estrutura de repositórios e organização de código
- Firmware e aplicações de supervisão
- Interfaces homem-máquina (HMI) e APIs
- Build, testes e versionamento
- Logs, telemetria e diagnóstico

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Visão geral](visao-geral.md) | Objetivos, stack e fronteiras da área |

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Comandos de movimento | Controle | Setpoints, modos e estados |
| Feedback de sensores | Eletrônica | Leituras brutas e calibradas |
| Limites físicos | Mecânica | Envelopes e restrições de junta |

!!! note "Padrão de registro"
    Documente decisões de software com motivação técnica, alternativas consideradas e impacto nas demais áreas.
