# Código

Estrutura de implementação do software do braço robótico: **Python** na camada de supervisão/interface e **C** no controle de periféricos e sensores.

## Diretrizes

- **Inputs e outputs** explícitos em cada módulo
- Python **orquestra e exibe**; C **aciona hardware**

## Visão geral da execução

```text
┌─────────────────────────────────┐
│  Python (supervisão / UI)       │
│  - telas e status               │
│  - comandos / setpoints         │
│  - logs                         │
└────────────────┬────────────────┘
                 │ IPC (JSON): setpoint / telemetria
                 ▼
┌─────────────────────────────────┐
│  C (runtime)                    │
│  1. lê sensores (feedback)      │
│  2. PID malha fechada           │  
│  3. escreve PWM (PCA9685)       │
│  4. reporta estado ao Python    │
└─────────────────────────────────┘
```

**PID**, no laço periódico do runtime (`runtime/pid.c`), entre a leitura dos sensores e a escrita no PCA9685.

| Camada | Papel na malha |
| ------ | -------------- |
| Python | Envia **setpoint** (ângulo/missão desejados) e **mostra** erro, saída e estado |
| C — sensores | Mede a **posição/velocidade atual** (feedback) |
| C — PID | Calcula `u = Kp·e + Ki·∫e + Kd·de/dt` |
| C — HAL | Aplica `u` como **PWM** nos servos / broca |

```text
setpoint (Python) ──► erro e = r − y ──► PID ──► PWM ──► planta (junta)
                         ▲                              │
                         └──────── feedback y ──────────┘
                                   (sensores)
```

## Árvore de pastas

```text
software/
├── app/                      # Python — UI e orquestração
│   ├── main.py               # ponto de entrada
│   ├── ui.py                 # telas / painel de status
│   ├── bridge.py             # sobe o binário C e troca mensagens
│   └── protocol.py           # contrato de comandos e telemetria
├── runtime/                  # C — periféricos, sensores e PID
│   ├── main.c                # loop: sensor → PID → PWM → telemetria
│   ├── protocol.c / .h       # parse/serialize JSON-line
│   ├── pid.c / .h            # malha fechada PID por junta
│   ├── hal_pca9685.c / .h    # PWM via I²C
│   ├── joints.c / .h         # juntas (servos)
│   ├── drill.c / .h          # motor de perfuração
│   └── sensors.c / .h        # feedback (leitura atual)
└── build/                    # binário gerado (ex.: arm_runtime)
```

---

## 1. Contrato de comunicação (IPC)

Python e C trocam **uma mensagem JSON por linha** (JSON Lines).  
**Input (Python → C):** comando de missão ou setpoint.  
**Output (C → Python):** telemetria e confirmação de estado.

```python
# app/protocol.py
COMMANDS = {
    "ping": {},
    "home": {},
    "set_joint": {"joint": int, "angle_deg": float},
    "drill": {"enable": bool, "duty": float},
    "mission": {"action": str},  # start_sampling | abort | stow
}

TELEMETRY = {
    "ok": bool,
    "state": str,          # IDLE, DRILLING, SAFE_STOP, ...
    "joints_deg": list,    # ângulos atuais
    "drill_on": bool,
    "sensors": dict,       # leituras brutas/calibradas
    "msg": str,
}
```

```c
/* runtime/protocol.h */
typedef struct {
    char type[32];     /* set_joint | drill | mission | ping */
    int  joint;
    float angle_deg;
    int  drill_enable;
    float drill_duty;
    char mission_action[32];
} Command;

typedef struct {
    int ok;
    char state[32];
    float joints_deg[6];
    int drill_on;
    char msg[128];
} Telemetry;
```

---

## 2. Runtime em C — laço de malha fechada

O binário C roda em ciclo periódico. Comandos do Python só **atualizam o setpoint**; o PID roda sempre no C.

```c
/* runtime/main.c — esqueleto com PID */
#include "protocol.h"
#include "pid.h"
#include "joints.h"
#include "drill.h"
#include "sensors.h"

int main(void) {
    Command cmd;
    Telemetry tel = {0};
    float setpoint[6] = {0};
    float y[6], u[6];
    PidState pid[6];

    hal_init();
    pid_init_all(pid);          /* Kp, Ki, Kd por junta */
    sensors_init();

    snprintf(tel.state, sizeof tel.state, "IDLE");

    while (1) {
        /* 1) novos setpoints vindos do Python */
        if (protocol_read_command(&cmd))
            runtime_update_setpoint(&cmd, setpoint, &tel);

        /* 2) feedback */
        sensors_read_joints(y);

        /* 3) malha fechada PID: u = f(r, y) */
        for (int i = 0; i < 6; i++)
            u[i] = pid_step(&pid[i], setpoint[i], y[i], DT_S);

        /* 4) atua no hardware */
        joints_apply_effort(u);
        sensors_read(&tel);
        for (int i = 0; i < 6; i++)
            tel.joints_deg[i] = y[i];

        protocol_write_telemetry(&tel);
        sleep_dt(DT_S);         /* período fixo da malha */
    }
    return 0;
}
```

---

## 3. Módulo PID (C) — malha fechada

Implementação enxuta do controlador. Ganhos e discretização vêm do referencial da área de **Controle**.

```c
/* runtime/pid.h */
typedef struct {
    float kp, ki, kd;
    float i_acc;       /* acumulador integral */
    float prev_e;      /* erro anterior */
    float u_min, u_max;
} PidState;

void  pid_init_all(PidState pid[6]);
float pid_step(PidState *s, float setpoint, float measured, float dt);
```

```c
/* runtime/pid.c */
float pid_step(PidState *s, float r, float y, float dt) {
    float e = r - y;                 /* erro */
    s->i_acc += e * dt;              /* termo integral */
    float d = (e - s->prev_e) / dt;  /* termo derivativo */
    s->prev_e = e;

    float u = s->kp * e + s->ki * s->i_acc + s->kd * d;

    /* saturação da saída (anti-windup simplificado) */
    if (u > s->u_max) u = s->u_max;
    if (u < s->u_min) u = s->u_min;
    return u;
}
```

**Inputs:** `setpoint` (r), `measured` (y), `dt`.  
**Output:** esforço `u` (mapeado para PWM no HAL).

---

## 4. Atuação nas juntas e broca (C)

Depois do PID, o esforço vai para o PCA9685. A UI Python **não** escreve PWM diretamente.

```c
/* runtime/joints.h */
void joints_init(void);
int  joints_apply_effort(const float u[6]); /* saída do PID → PWM */
void joints_get_angles(float out_deg[6]);

/* runtime/drill.h */
void drill_init(void);
int  drill_set(int enable, float duty); /* duty 0.0..1.0 */
```

```c
/* runtime/joints.c */
int joints_apply_effort(const float u[6]) {
    for (int j = 0; j < 6; j++) {
        if (pca9685_set_channel_effort(j, u[j]) != 0)
            return -1;
    }
    return 0;
}
```

---

## 5. Bridge Python — sobe o C e troca mensagens

A bridge inicia o runtime C como subprocesso e envia/recebe linhas JSON.

```python
# app/bridge.py
import json
import subprocess
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "build" / "arm_runtime"

class ArmBridge:
    def __init__(self):
        self.proc = subprocess.Popen(
            [str(RUNTIME)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def send(self, payload: dict) -> dict:
        line = json.dumps(payload, ensure_ascii=False)
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()
        raw = self.proc.stdout.readline()
        return json.loads(raw)

    def close(self):
        self.proc.terminate()
```

**Inputs:** `payload` (`dict` de comando).  
**Outputs:** telemetria (`dict`) vinda do C.

---

## 6. UI Python — painel de status

Camada responsável por telas organizadas: estado da missão, ângulos, broca e sensores.

```python
# app/ui.py
def render_status(tel: dict) -> None:
    print("=" * 40)
    print(f"Estado : {tel.get('state', '?')}")
    print(f"Juntas : {tel.get('joints_deg', [])}")
    print(f"Broca  : {'ON' if tel.get('drill_on') else 'OFF'}")
    print(f"Sensores: {tel.get('sensors', {})}")
    print(f"Msg    : {tel.get('msg', '')}")
    print("=" * 40)
```

!!! tip "Evolução da UI"
    O esqueleto acima é CLI. Pode evoluir para `textual` / `rich` / GUI sem mudar o contrato com o C.

---

## 7. Main Python — sistema de execução

Ponto de entrada: sobe o C, envia missões e atualiza a tela com a telemetria.

```python
# app/main.py
from bridge import ArmBridge
from ui import render_status

def main():
    arm = ArmBridge()
    try:
        tel = arm.send({"type": "ping"})
        render_status(tel)

        tel = arm.send({"type": "mission", "action": "start_sampling"})
        render_status(tel)

        tel = arm.send({"type": "set_joint", "joint": 0, "angle_deg": 45.0})
        render_status(tel)
    finally:
        arm.close()

if __name__ == "__main__":
    main()
```

---

## 8. Fluxo resumido

```text
1. python app/main.py
2. ArmBridge inicia build/arm_runtime (C)
3. Python envia setpoint / missão (JSON)
4. C em loop: sensores → PID → PWM (PCA9685)
5. C devolve telemetria → Python atualiza a tela
```

## Inputs e outputs por camada

| Camada | Inputs | Outputs |
| ------ | ------ | ------- |
| Python UI | telemetria | telas / logs |
| Python bridge | comandos / setpoints | JSON para o C |
| C protocol | JSON | `Command` / `Telemetry` |
| C PID | setpoint `r`, feedback `y`, `dt` | esforço `u` |
| C HAL | esforço `u` | PWM I²C, GPIO |

## Registros

| Módulo | Linguagem | Status | Observação |
| ------ | --------- | ------ | ---------- |
| `app/protocol.py` | Python | Modelado | Contrato IPC |
| `app/bridge.py` | Python | Modelado | Sobe e fala com o C |
| `app/ui.py` | Python | Modelado | Painel de status |
| `app/main.py` | Python | Modelado | Orquestração |
| `runtime/main.c` | C | Modelado | Loop sensor → PID → PWM |
| `runtime/pid.c` | C | Modelado | Malha fechada por junta |
| `runtime/joints.c` | C | Modelado | Esforço → PCA9685 |
| `runtime/drill.c` | C | Modelado | Perfuração |
| `runtime/sensors.c` | C | Em definição | Feedback da malha |

!!! note "Alinhamento com Controle"
    `Kp`, `Ki`, `Kd`, `dt` e limites de saturação são definidos na área de Controle e prontificados em `runtime/pid.c`. O Python apenas envia setpoints e exibe o resultado da malha.
