# Aula 07 — 30/Set — Estágio 3 (Semana 1)

## Retomando da aula (e do Estágio) anterior

Na aula passada concluímos `calc`, nossa LP de expressões infixas com
aritmética simples. 

No diretório `calc-v2` você encontrará a implementação atualizada de `calc` de
acordo com as decisões que tomamos sobre sintaxe e sobre a produção da AST
(precedência, associatividade, aridade, etc). Em `calc-v2/README.md` documentei
isso, parcialmente.

Nosso foco, contudo, foi na _sintaxe_ da LP. Nesta aula, vamos mudar nossa
atenção para a semântica.  

## Formalização da Semântica

Nas aulas anteriores, especificamos a semântica da LP por regras de transição.
Na prática, trata-se de uma semântica operacional small-step. Nesta parte do curso, faremos a transição para regras de semântica operacional big-step.

Leia o arquivo com a [Parte 1 de Semântica Operacional Big-Step](semantica-operacional-big-step-p1.md). É um mínimo ajuste sobre o que
usei em sala de aula na Aula 07. Ainda farei novos ajustes (em relação ao que
falamos em sala de aula), então fiquem atentos.
