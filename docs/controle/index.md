# Controle

Área responsável pela cinemática, dinâmicas relevantes, malhas de controle e validação do movimento do braço robótico.

## Escopo

- Modelagem cinemática e jacobianos
- Estratégias de controle (posição, velocidade, torque)
- Calibração de juntas e sensores
- Trajetórias e planejamento de movimento
- Ensaios de validação e métricas de desempenho

## Documentos desta área

| Documento | Descrição |
| --------- | --------- |
| [Visão geral](visao-geral.md) | Objetivos, modelos e critérios de aceite |

## Integrações

| Interface | Área parceira | Conteúdo típico |
| --------- | ------------- | --------------- |
| Setpoints e modos | Software | Comandos e estados |
| Atuadores e encoders | Eletrônica | Sinais e resolução |
| Geometria e limites | Mecânica | Comprimentos e batentes |

!!! warning "Segurança"
    Qualquer alteração em ganhos, limites ou trajetórias deve registrar risco, envelope seguro e procedimento de teste.
