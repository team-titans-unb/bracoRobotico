# Diagramas

Diagramas de software do projeto conceitual do manipulador (braço robótico) para a subtarefa de **amostragem profunda (Deep Sampling)** da ERC, conforme o alinhamento inicial e o edital do Projeto Trainee Rover Titans.

## Contexto operacional

O manipulador é projetado para:

- Coletar amostra de até **30 cm** de profundidade
- Depositar a amostra no contêiner embarcado do rover
- Operar com **até 6 GDL**, servos **MG996R** e motor de perfuração dedicado
- Ser controlado por **Raspberry Pi 3** + driver **PCA9685PW (I²C)**

## Diagramas

| Diagrama | Objetivo | Revisão | Status |
| -------- | -------- | ------- | ------ |
| [Arquitetura](#diagrama-de-arquitetura) | Camadas, módulos e interfaces de hardware/software | R01 | Modelado |
| [Máquina de estados](#diagrama-de-maquina-de-estados) | Modos de operação e transições seguras | R01 | Modelado |
| [Sequência](#diagrama-de-sequencia) | Fluxo da amostragem profunda | R01 | Modelado |

---

## Diagrama de arquitetura

Visão em camadas do sistema embarcado. A supervisão de missão e a máquina de estados residem na Raspberry Pi 3; o PCA9685 gera PWM para as juntas; o motor de perfuração é acionado por canal dedicado.

```mermaid
flowchart TB
  subgraph SUPER["Camada de missão"]
    OP["Operador / Rover<br/>comando de missão"]
    MM["Mission Manager<br/>Raspberry Pi 3"]
  end

  subgraph APP["Camada de software"]
    SM["Máquina de estados"]
    TP["Planejador de trajetória<br/>setpoints de juntas"]
    CI["Interface de controle<br/>inputs / outputs"]
  end

  subgraph CTRL["Camada de controle"]
    PID["Malhas PID por junta<br/>posição / velocidade"]
  end

  subgraph HW["Camada de hardware"]
    PCA["PCA9685PW<br/>PWM via I²C"]
    SRV["Servos MG996R<br/>juntas do braço ≤ 6 GDL"]
    DRL["Motor de perfuração<br/>efetuador"]
  end

  subgraph MEC["Camada mecânica"]
    ARM["Links + juntas<br/>alcance ≤ 80 cm"]
    EE["Ferramenta de amostragem<br/>perfuração profunda"]
  end

  OP --> MM
  MM --> SM
  SM --> TP
  TP --> CI
  CI --> PID
  PID --> PCA
  PCA --> SRV
  PCA --> DRL
  SRV --> ARM
  DRL --> EE
  ARM --> EE
```

### Interfaces principais

| Origem | Destino | Interface | Conteúdo |
| ------ | ------- | --------- | -------- |
| Mission Manager | Máquina de estados | Eventos de missão | Iniciar amostragem, abortar, concluir |
| Planejador | Controle | Setpoints | Ângulos/posições de junta alvo |
| Controle | PCA9685 | I²C | Canais PWM das juntas e da broca |
| PCA9685 | MG996R | PWM | Acionamento das juntas |
| PCA9685 / driver | Motor de perfuração | PWM / potência | Perfuração até ~30 cm |
| Mecânica | Controle / Software | Parâmetros | Limites, batentes, envelope |

!!! note "Hipótese do edital"
    A base do manipulador é admitida **engastada** em superfície horizontal. Contêiner, pesagem e fotos pertencem ao contexto do rover e aparecem na sequência operacional.

---

## Diagrama de máquina de estados

Estados de operação do software embarcado durante a subtarefa de amostragem profunda. Qualquer falha crítica leva a `SAFE_STOP`.

```mermaid
stateDiagram-v2
  [*] --> BOOT

  BOOT --> IDLE: inicialização OK
  BOOT --> SAFE_STOP: falha de boot

  IDLE --> HOMING: comando home
  HOMING --> READY: juntas na referência
  HOMING --> SAFE_STOP: falha de homing

  READY --> APPROACH: iniciar amostragem
  READY --> IDLE: standby

  APPROACH --> ALIGN_DRILL: pose sobre o ponto
  ALIGN_DRILL --> DRILLING: alinhamento OK
  DRILLING --> EXTRACT: profundidade alvo (~30 cm)
  EXTRACT --> TO_CONTAINER: amostra retida
  TO_CONTAINER --> DEPOSIT: pose sobre o contêiner
  DEPOSIT --> STOW: amostra depositada
  STOW --> COMPLETE: braço recolhido
  COMPLETE --> IDLE: reset de missão

  APPROACH --> SAFE_STOP: colisão / limite / abort
  ALIGN_DRILL --> SAFE_STOP: falha de alinhamento
  DRILLING --> SAFE_STOP: falha de perfuração
  EXTRACT --> SAFE_STOP: perda de amostra / falha
  TO_CONTAINER --> SAFE_STOP: trajetória inválida
  DEPOSIT --> SAFE_STOP: falha ao depositar
  STOW --> SAFE_STOP: falha ao recolher

  SAFE_STOP --> IDLE: reset autorizado
```

### Descrição dos estados

| Estado | Descrição |
| ------ | --------- |
| `BOOT` | Inicializa RPi, I²C/PCA9685 e verifica canais |
| `IDLE` | Aguarda comando; motores em segurança |
| `HOMING` | Move juntas para pose de referência |
| `READY` | Pronto para missão de amostragem |
| `APPROACH` | Aproxima o efetuador do ponto de amostragem |
| `ALIGN_DRILL` | Alinha a ferramenta de perfuração ao solo |
| `DRILLING` | Perfura até a profundidade alvo (meta > 300 mm) |
| `EXTRACT` | Retrai o núcleo / retém a amostra |
| `TO_CONTAINER` | Transporta a amostra até o contêiner embarcado |
| `DEPOSIT` | Deposita a amostra no contêiner |
| `STOW` | Recolhe o braço para pose segura de transporte |
| `COMPLETE` | Missão concluída com sucesso |
| `SAFE_STOP` | Para atuadores e aguarda intervenção |

---

## Diagrama de sequência

Fluxo principal da amostragem profunda, do comando de missão até o depósito no contêiner.

```mermaid
sequenceDiagram
  autonumber
  actor Op as Operador / Rover
  participant MM as Mission Manager<br/>(RPi 3)
  participant SM as Máquina de estados
  participant CTRL as Controle PID
  participant PCA as PCA9685 (I²C)
  participant SRV as Servos MG996R
  participant DRL as Motor de perfuração

  Op->>MM: Iniciar Deep Sampling
  MM->>SM: evento START_SAMPLING
  SM->>SM: READY → APPROACH
  SM->>CTRL: setpoints de aproximação
  CTRL->>PCA: PWM juntas
  PCA->>SRV: movimento até o ponto
  SRV-->>CTRL: pose alcançada
  CTRL-->>SM: APPROACH_OK

  SM->>SM: ALIGN_DRILL
  SM->>CTRL: setpoints de alinhamento
  CTRL->>PCA: PWM juntas
  PCA->>SRV: ajuste de orientação
  SRV-->>SM: ALIGN_OK

  SM->>SM: DRILLING
  SM->>CTRL: habilitar broca + avanço
  CTRL->>PCA: PWM broca / eixo de avanço
  PCA->>DRL: perfuração (~30 cm)
  DRL-->>SM: DEPTH_OK

  SM->>SM: EXTRACT
  SM->>CTRL: retração com amostra
  CTRL->>PCA: PWM juntas / broca off
  PCA->>SRV: extrair núcleo
  SRV-->>SM: SAMPLE_HELD

  SM->>SM: TO_CONTAINER → DEPOSIT
  SM->>CTRL: trajetória até contêiner
  CTRL->>PCA: PWM juntas
  PCA->>SRV: mover e depositar
  SRV-->>SM: DEPOSIT_OK

  SM->>SM: STOW → COMPLETE
  SM->>CTRL: pose de recolhimento
  CTRL->>PCA: PWM juntas
  PCA->>SRV: stow
  SRV-->>SM: STOW_OK
  SM-->>MM: missão concluída
  MM-->>Op: Deep Sampling OK

  Note over Op,DRL: Em falha (limite, I²C, timeout): transição para SAFE_STOP e reporte ao Mission Manager
```

### Relação com o cenário ERC

| Passo do cenário ERC | Cobertura no manipulador |
| -------------------- | ------------------------ |
| Chegar ao local / fotos / pesagem / retorno | Contexto do rover (fora do escopo direto do braço) |
| Realizar amostragem (núcleo perfurado) | Estados `ALIGN_DRILL` → `DRILLING` → `EXTRACT` |
| Colocar amostra no contêiner | Estados `TO_CONTAINER` → `DEPOSIT` |
| Ferramenta especial de perfuração no braço | Motor de perfuração + efetuador |

---

## Registros

| Diagrama | Revisão | Formato | Observação |
| -------- | ------- | ------- | ---------- |
| Arquitetura | R01 | Mermaid | Base conceitual RPi 3 + PCA9685 + MG996R |
| Máquina de estados | R01 | Mermaid | Inclui `SAFE_STOP` e fluxo Deep Sampling |
| Sequência | R01 | Mermaid | Fluxo feliz + nota de falha |

!!! tip "Próximos refinamentos"
    Detalhar canais PWM do PCA9685, assinatura exata dos inputs/outputs das funções de controle e tempos máximos por estado após a definição da malha PID.
