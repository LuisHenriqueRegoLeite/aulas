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

Na nossa aula 02, mostramos como formalizar a semântica 
