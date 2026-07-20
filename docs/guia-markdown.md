# Guia Markdown

Referência rápida de Markdown para manter a documentação do projeto uniforme. Use este padrão ao criar ou editar páginas.

## Sumário

- [Títulos](#titulos)
- [Ênfase](#enfase)
- [Listas](#listas)
- [Links e imagens](#links-e-imagens)
- [Código](#codigo)
- [Tabelas](#tabelas)
- [Citações e notas](#citacoes-e-notas)
- [Linha horizontal](#linha-horizontal)

## Títulos

```markdown
# Título nível 1
## Título nível 2
### Título nível 3
#### Título nível 4
```

No site, isso renderiza como hierarquia de seções. Use **um único** `#` por página (título principal) e organize o restante com `##` / `###`.

!!! tip "Boas práticas"
    Títulos curtos, objetivos e sem numeração manual — o MkDocs já gera a numeração visual e o sumário lateral.

## Ênfase

```markdown
*itálico* ou _itálico_
**negrito** ou __negrito__
**_negrito itálico_**
~~riscado~~
`código inline`
```

*itálico* · **negrito** · **_negrito itálico_** · ~~riscado~~ · `código inline`

## Listas

```markdown
- Item A
- Item B
  - Subitem B1
  - Subitem B2

1. Primeiro
2. Segundo
3. Terceiro

- [ ] Pendente
- [x] Concluído
```

- Item A
- Item B
  - Subitem B1
  - Subitem B2

1. Primeiro
2. Segundo
3. Terceiro

- [ ] Pendente
- [x] Concluído

## Links e imagens

```markdown
[Documentação MkDocs](https://www.mkdocs.org)
[Visão geral de Software](software/visao-geral.md)

![Texto alternativo](caminho/da/imagem.png)
```

[Documentação MkDocs](https://www.mkdocs.org) · [Visão geral de Software](software/visao-geral.md)

## Código

Inline: `mkdocs serve`

Bloco com linguagem:

````markdown
```python
def posicao_efetuador(q):
    """Calcula a pose a partir das juntas."""
    return cinematica_direta(q)
```
````

```python
def posicao_efetuador(q):
    """Calcula a pose a partir das juntas."""
    return cinematica_direta(q)
```

## Tabelas

```markdown
| Parâmetro | Valor | Unidade |
| --------- | ----- | ------- |
| Junta 1   | ±90   | grau    |
| Junta 2   | ±120  | grau    |
```

| Parâmetro | Valor | Unidade |
| --------- | ----- | ------- |
| Junta 1   | ±90   | grau    |
| Junta 2   | ±120  | grau    |

## Citações e notas

```markdown
> Decisão: adotar encoder absoluto nas juntas de base.

!!! note "Nota"
    Informação complementar.

!!! warning "Atenção"
    Risco operacional ou limite técnico.

!!! danger "Perigo"
    Procedimento com risco elétrico ou mecânico.
```

> Decisão: adotar encoder absoluto nas juntas de base.

!!! note "Nota"
    Informação complementar.

!!! warning "Atenção"
    Risco operacional ou limite técnico.

!!! danger "Perigo"
    Procedimento com risco elétrico ou mecânico.

## Linha horizontal

```markdown
---
```

---

## Padrão editorial do projeto

| Elemento | Recomendação |
| -------- | ------------ |
| Idioma | Português (Brasil) |
| Tom | Técnico, direto, corporativo |
| Unidades | SI (mm, kg, V, A, rad ou grau — declarar) |
| Decisões | Registrar contexto + alternativa + impacto |
| Figuras | Sempre com legenda e fonte/revisão |
| Status | Usar tabelas com “Em definição / Em andamento / Congelado” |
