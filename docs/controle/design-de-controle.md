# Design de controle

Projeto das funções de controle e da malha PID a serem prontificadas em código.

## Onde a malha fecha no software

A malha **fechada com PID** roda no **runtime C** (`software/runtime/pid.c`), não no Python.

| Etapa | Onde | O quê |
| ----- | ---- | ----- |
| Setpoint `r` | Python → C (IPC) | Ângulo/missão desejados |
| Feedback `y` | C (`sensors`) | Posição/velocidade medida |
| Controle PID | C (`pid`) | `u = Kp·e + Ki·∫e + Kd·de/dt` |
| Atuação | C (`joints` / PCA9685) | PWM nos MG996R |
| Monitoramento | Python (UI) | Exibe `r`, `y`, estado e erros |

## Escopo do alinhamento

- Estrutura da malha PID por junta
- Funções de controle a modelar em código C
- Definição clara de inputs (`r`, `y`, `dt`) e output (`u`)
- Critérios de desempenho e segurança (saturação, `SAFE_STOP`)

## Registros

| Elemento de design | Status | Observação |
| ------------------ | ------ | ---------- |
| Malha PID | Modelado (interface) | Implementação em `runtime/pid.c` |
| Funções de controle | Em definição | Ganhos Kp/Ki/Kd a sintonizar |
| Período da malha `dt` | Em definição | Fixar no loop do `main.c` |

!!! warning "Segurança"
    Alterações de ganhos ou limites devem registrar risco, envelope seguro e procedimento de teste.

!!! note "Encaminhamento para Software"
    Controle define a matemática e os ganhos; Software prontifica em `runtime/pid.c` e mantém o Python só como supervisão/UI.
