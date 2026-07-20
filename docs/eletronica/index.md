# Eletrônica

Área responsável pelo hardware elétrico e eletrônico: alimentação, drivers, sensores, proteção e integração com o restante do sistema.

## Escopo

- Diagrama elétrico e esquemáticos
- Seleção de microcontroladores, drivers e sensores
- Fonte, distribuição de potência e proteções
- PCB / protoboard e cabeamento
- Ensaios elétricos e de integridade de sinal

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Visão geral](visao-geral.md) | Arquitetura elétrica e interfaces |

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Barramentos e I/O | Software | Protocolos e pinagem |
| Realimentação | Controle | Encoders, corrente, tensão |
| Espaço e fixação | Mecânica | Volumes e conectores |

!!! danger "Segurança elétrica"
    Documente tensões, correntes máximas e procedimentos de energização antes de qualquer ensaio com motores.
