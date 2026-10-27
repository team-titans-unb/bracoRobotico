# Robô Bio — Seguidor de Linha

<div class="hero-meta" markdown="0">
  <span><strong>Time:</strong> Robotics Titans UnB</span>
  <span><strong>Origem:</strong> FSE — FCTE/UnB</span>
  <span><strong>Versão atual:</strong> V2 (em desenvolvimento)</span>
</div>

![Robô Bio V2 montado, com placas solares e servos MG996R](assets/imagens/capa.jpeg){ .figura-destaque }

O **Robô Bio** é um seguidor de linha autônomo desenvolvido inicialmente como trabalho final da disciplina **Fundamentos de Sistemas Embarcados (FSE)**, da Faculdade de Ciências e Tecnologias em Engenharia (**FCTE/UnB**).

O projeto partiu da **V1** PID clássico, sensores de refletância e telemetria via ThingsBoard, passou por um novo chassi na **V2** e segue em direção a um robô mais robusto: calibração de PID por **algoritmos bioinspirados** e delimitação do trajeto por **visão computacional**.

## Linha do tempo

| Etapa | Destaques | Status |
| ----- | --------- | ------ |
| [Robô Bio V1](projeto/v1.md) | ESP32 + ESP-IDF, sensores de refletância, PID manual, telemetria MQTT/ThingsBoard | Concluída |
| [Robô Bio V2](projeto/v2.md) | Novo chassi impresso em 3D, Raspberry Pi 3, PCA9685PW, 12 servos MG996R, placas solares | Em desenvolvimento |
| Próximos passos | PID por algoritmos bioinspirados, visão computacional do trajeto | Planejado |

## Áreas de desenvolvimento

<div class="area-grid" markdown="0">
  <a class="area-card" href="mecanica/">
    <span class="area-card__label">Área 01</span>
    <span class="area-card__title">Mecânica</span>
    <span class="area-card__desc">Chassi da V2, impressão 3D em PLA/PETG e conversão dos servos para rotação contínua.</span>
  </a>
  <a class="area-card" href="eletronica/">
    <span class="area-card__label">Área 02</span>
    <span class="area-card__title">Eletrônica</span>
    <span class="area-card__desc">Raspberry Pi 3, driver PWM PCA9685PW, 12 servos MG996R e placas solares.</span>
  </a>
  <a class="area-card" href="software/">
    <span class="area-card__label">Área 03</span>
    <span class="area-card__title">Software e controle</span>
    <span class="area-card__desc">Loop em tempo real, controle PID, telemetria e visão computacional.</span>
  </a>
  <a class="area-card" href="galeria/">
    <span class="area-card__label">Registro</span>
    <span class="area-card__title">Galeria</span>
    <span class="area-card__desc">Fotos da montagem, dos ajustes nos motores e da evolução mecânica.</span>
  </a>
</div>

## Equipe

| Integrante | Papel |
| ---------- | ----- |
| [Felipe das Neves](https://github.com/FelipeFreire-gf) | Desenvolvimento do projeto (mecânica, eletrônica e software) |

!!! tip "Contribuição"
    Mantenha títulos objetivos, registre decisões com contexto e evite duplicar conteúdo entre áreas. Quando um tópico for interdisciplinar, referencie a área dona do conteúdo.
