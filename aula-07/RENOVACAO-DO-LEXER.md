# Renovação do Lexer

Este foi um assunto à parte na aula de hoje: a renovação do Lexer.

É importante que vocês leiam a nova implementação do lexer (arquivo `lexer.py`)
e todas as definições a ele relativas no arquivo `tipos.py`. A renovação foi
significativa, porque deixamos de programar no estilo _stringly-typed_ que
usamos para manter as primeiras versões o mais simples que fosse possível.
Agora temos um tipo `Token` (defindo com um `dataclass` _frozen_) e um tipo
`TokenType` definido como um enumerado. Isso significa que agora podemos
consultar o tipo do token sem precisar analisar a string.

Além disso, passamos a usar regexes para a análise léxica propriamente dita. Em
particular, usamos a abordagem de formar uma regex única a partir de regexes
independentes e simples para cada tipo de token. 

> Relembre que discutimos em sala de aula a ordem em que os tipos de tokens e
> respectivas regexes precisam ser listadas no `TOKEN_SPEC`, para garantir que
> o casamento do texto do token seja feito corretamente, evitando detectar
> tipos de tokens erroneamente (por exemplo, para que o lexer não confunda `**`
> com dois operadores `*`).

Por fim, em uma abordagem que não é padrão, mas que é bastante interessante,
defini predicados para os tokens que precisamos reconhecer em outras partes do
interpretador. Isso permite testar o tipo de qualquer token de forma simples
(veja ainda como esses predicados são criados com a função `match_type` no
arquivo `tipos.py`).
