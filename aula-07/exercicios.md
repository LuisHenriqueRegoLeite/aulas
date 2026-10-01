# Exercícios (Aula 07)

A versão v3 de `calc` ainda tem vários pequenos ajustes que são necessários.
Você deve tratar dois deles neste exercício.

- o operador `**` e a operação de exponenciação;
- o operador `-` unário e sua implementação.

1. `[q13]` Observe que a especificação de `calc-v3` não inclui explicitamente o
   operador `**`. Nem está listado como um dos operadores da regra `Op`, nem há
   regras específicas para tratar do fato de que a exponenciação é parcial; ou
   seja, que para alguns casos conhecidos, a exponenciação não está definida.

   Ajuste a especificação da semântica de `calc` para que lide explicitamente
   com os casos abaixo em que a exponenciação não está definida:
   - $0^{-1}$ é indefinida (divisão por zero);
   - $-1^{0.5}$ não é real;
   - $0^{0}$ é ambíguo.

   Para cada um desses casos, o valor produzido pela avaliação deve ser
   $\mathrm{erro}$. Por ora, não é necessário implementar o avaliador (você
   fará isso no terceiro exercício desta lista).

2. `[q14]` Nossa linguagem, também não tem um operador `-` unário (aquele que
   nos permite escrever `-1` ou `-x`, em outras linguagens. Mas observe que o
   caso aqui é mais complexo que o do exercício anterior. Isso ocorre porque
   além de não ser binário é preciso pensar no nível de precedência do operador
   `-` unário. Qual AST desejamos para `- 2 ** 2`, por exemplo? Faça uma
   pesquisa e veja como Python e JS tratam essa questão. Faça sua escolha e
   especifique a sintaxe e a AST necessárias para isso. Especifique as regras
   de inferência (semântica) para lidar com o operador unário. Nomeie as regras
   de forma semelhante à que usamos para as regras anteriores.

3. `[q15]` Implemente `calv-v4` para incorporar os dois operadores que você
   especificou acima. Lembre que será necessário rever os três níveis da
   implementação, desde o nível léxico ao `eval()`.
