# Mecânica

Área responsável pelo projeto estrutural, materiais, fabricação e montagem do braço robótico.

## Escopo

- Modelagem CAD e desenhos técnicos
- Seleção de materiais e processos de fabricação
- Dimensionamento estrutural e folgas
- Montagem, alinhamento e manutenção
- Restrições mecânicas para controle e eletrônica

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Visão geral](visao-geral.md) | Requisitos mecânicos e entregáveis |

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Envelope de movimento | Controle | Limites e singularidades |
| Fixação de sensores/motores | Eletrônica | Furos, bases e clearance |
| Massa e inércia | Controle / Software | Parâmetros do modelo |

!!! note "Controle de versão de CAD"
    Registre revisão do modelo (ex.: `R01`, `R02`) sempre que houver mudança dimensional relevante.
