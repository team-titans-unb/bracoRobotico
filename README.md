# Robô Bio — Seguidor de Linha

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MkDocs](https://img.shields.io/badge/MkDocs-Material-526CFE?style=for-the-badge&logo=materialformkdocs&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-221F1F?style=for-the-badge&logo=githubpages&logoColor=white)

[![GitHub](https://img.shields.io/badge/GitHub-Repositório-181717?style=for-the-badge&logo=github)](https://github.com/team-titans-unb/bracoRobotico)
[![Documentação](https://img.shields.io/badge/Docs-MkDocs-526CFE?style=for-the-badge&logo=materialformkdocs&logoColor=white)](https://team-titans-unb.github.io/bracoRobotico/)
[![Organização](https://img.shields.io/badge/Org-team--titans--unb-0B1F33?style=for-the-badge&logo=github)](https://github.com/team-titans-unb)

<img src="docs/assets/imagens/capa.jpeg" alt="Robô Bio V2" width="360"/>

</div>

---

**Documentação técnica do Robô Bio, seguidor de linha do time Robotics Titans (UnB), organizada nas áreas de Mecânica, Eletrônica e Software e controle.**

---

## Sobre o Projeto

O **Robô Bio** é um seguidor de linha autônomo desenvolvido inicialmente como trabalho final da disciplina **Fundamentos de Sistemas Embarcados (FSE)**, da FCTE/UnB, sob orientação do professor **Dr. Renato Coral**.

| Versão | Resumo | Status |
|--------|--------|--------|
| **V1** | ESP32 + ESP-IDF, sensores de refletância, PID com ajuste manual, telemetria Wi-Fi/MQTT no ThingsBoard | Concluída |
| **V2** | Novo chassi impresso em PLA/PETG, Raspberry Pi 3, PCA9685PW, 12 servos MG996R e 4 placas solares | Em desenvolvimento |
| **Próximos passos** | Constantes de PID por algoritmos bioinspirados e visão computacional do trajeto | Planejado |

## Documentação

**Site de Documentação**: [https://team-titans-unb.github.io/bracoRobotico/](https://team-titans-unb.github.io/bracoRobotico/)

A documentação inclui:

- Visão geral e linha do tempo do projeto
- Páginas das versões V1 e V2
- Páginas por área técnica (Mecânica, Eletrônica e Software e controle)
- Galeria de fotos da montagem
- Guia Markdown com o padrão editorial da equipe

---

## Estrutura do Projeto

```text
bracoRobotico/
├── docs/                         # Conteúdo da documentação (Markdown)
│   ├── index.md                  # Página inicial
│   ├── galeria.md                # Fotos do projeto
│   ├── guia-markdown.md          # Padrão editorial / cheatsheet
│   ├── projeto/                  # Robô Bio V1 e V2
│   ├── mecanica/                 # Área de Mecânica
│   ├── eletronica/               # Área de Eletrônica
│   ├── software/                 # Área de Software e controle
│   ├── assets/imagens/           # Fotos e renders
│   ├── javascripts/              # MathJax (fórmulas)
│   └── stylesheets/              # CSS corporativo
├── overrides/                    # Customizações do tema Material
│   └── partials/
├── .github/
│   └── workflows/
│       └── deploy.yml            # Deploy automático no GitHub Pages
├── mkdocs.yml                    # Configuração do MkDocs
├── requirements.txt              # Dependências Python
└── README.md
```

---

## Tecnologias Utilizadas

| Categoria | Tecnologias |
|-----------|-------------|
| **Documentação** | ![MkDocs](https://img.shields.io/badge/MkDocs-526CFE?style=flat&logo=materialformkdocs&logoColor=white) ![Material](https://img.shields.io/badge/Material-526CFE?style=flat&logo=materialformkdocs&logoColor=white) ![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white) |
| **Publicação** | ![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-221F1F?style=flat&logo=githubpages&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white) |
| **Robô** | ![ESP32](https://img.shields.io/badge/ESP32-E7352C?style=flat&logo=espressif&logoColor=white) ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberrypi&logoColor=white) ![MQTT](https://img.shields.io/badge/MQTT-660066?style=flat&logo=mqtt&logoColor=white) |

---

## Status das Áreas

| Área | Status | Descrição |
|------|--------|-----------|
| **Mecânica** | Montado | Chassi V2 e conversão dos servos |
| **Eletrônica** | Integrado | Raspberry Pi 3, PCA9685PW e placas solares; esquemático em definição |
| **Software e controle** | Em desenvolvimento | PID, telemetria, algoritmos bioinspirados e visão computacional |

---

## Equipe

**Robotics Titans | Universidade de Brasília (UnB)**

<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/FelipeFreire-gf">
        <img style="border-radius: 50%;" src="https://github.com/FelipeFreire-gf.png" width="120px;" alt="Felipe das Neves"/>
        <br />
        <sub><b>Felipe das Neves</b></sub>
      </a>
    </td>
  </tr>
</table>

</div>

---

## Contribuição

1. Atualize a documentação na área correspondente (`docs/projeto`, `docs/mecanica`, `docs/eletronica` ou `docs/software`)
2. Salve novas fotos em `docs/assets/imagens/`
3. Siga o padrão editorial em [`docs/guia-markdown.md`](docs/guia-markdown.md)
4. Valide localmente com `python -m mkdocs serve`
5. Faça push na `main` — o deploy no GitHub Pages ocorre automaticamente via Actions

---

## Licença

Este projeto é desenvolvido pelo time **Robotics Titans** no contexto da **Universidade de Brasília (UnB)**.

**Instituição**: Universidade de Brasília (UnB)  
**Time**: Robotics Titans  
**Projeto**: Robô Bio

---

<div align="center">

<sub>Robotics Titans UnB — Documentação do Robô Bio</sub>

</div>
