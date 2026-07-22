# Referencial teórico

Referencial teórico necessário ao funcionamento ideal do braço, com foco na modelagem da malha PID.

## Escopo do alinhamento

- Bases matemáticas para a malha de controle PID
- Hipóteses e simplificações adotadas
- Parâmetros e grandezas envolvidas no modelo
- Referências utilizadas

## Referencial teórico

O controlador PID serve para dirigir sinais ao braço de forma a compensar erros externos, como por exemplo o atrito das juntas. Ele compensa o erro do sistema utilizando três termos: proporcional, integral e diferencial. Considerando o erro em função do tempo $$e(t)$$, a função de PID pode ser definida como: 

$$u(t) = K_p*e(t) + K_i * \int{e(t)}{dt} + K_d * \frac{de}{dt}$$

...onde $$K_p$$, $$K_i$$ e $$K_d$$ são os pesos de cada termo na soma final.

A figura abaixo ilustra como a função $$u(t)$$ se encaixa no sistema. Perceba que o valor que o sistema retorna é reutilizado no cálculo do erro atual.

<img width="482" height="203" alt="image" src="https://github.com/user-attachments/assets/13040eb7-309a-45d1-8694-4f5c16bf7bbb" />

Para o braço robótico, serão necessários mais de um controlador PID, um para cada junta. Porém, as juntas afetam umas às outras, o que significa que estabilizar uma delas pode significar desbalancear outra. Isso requer implementar uma **matriz de controle PID**.

--TODO desenvolver matriz PID
--ainda sou noob nisso...

## Referência Bibliográfica
[Introduction: PID Controller Design (MATLAB & SIMULINK)](https://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlPID#27)

[Understanding PID Control](https://www.youtube.com/playlist?list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y)

## Registros

| Tópico | Status | Referência / anotação |
| ------ | ------ | --------------------- |
| Modelagem da malha PID | Em definição | — |
| Referencial das contas matemáticas | Em definição | — |

!!! tip "Padrão"
    Declare hipóteses, unidades e a faixa de validade de cada desenvolvimento.
