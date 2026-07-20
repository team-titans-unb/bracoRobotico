# Visão geral — Controle

## Objetivo

Garantir movimento preciso, estável e seguro do braço, com critérios claros de desempenho e rastreabilidade de parâmetros.

## Modelos previstos

| Modelo | Uso | Status |
| ------ | --- | ------ |
| Cinemática direta | Posição do efetuador | Em definição |
| Cinemática inversa | Ângulos de junta | Em definição |
| Dinâmica simplificada | Dimensionamento / simulação | Em definição |
| Malha de controle | Seguimento de referência | Em definição |

## Critérios de aceite (rascunho)

- Erro de posicionamento dentro da tolerância definida
- Ausência de oscilação persistente em regime
- Respeito a limites de velocidade e torque
- Recuperação previsível após falha de sensor (quando aplicável)

## Próximos registros

- [ ] Definir graus de liberdade e convenção de eixos
- [ ] Publicar diagrama de blocos da malha
- [ ] Registrar parâmetros iniciais (Kp, Ki, Kd / equivalentes)
- [ ] Planejar bancada de calibração
