### Integridade utilizando Pedersen commitments

Sendo $ x $ um valor como latência observada, é desejado o valor de $ s_x = x_1 + x_2 + ... + x_n $ representando a latência de diversos contratos e/ou medições ao longo do tempo.

Considerando que a informação armazenada é cifrada com o Pedersen commitment:

$$ cm_i = g^x_i h^r_i $$

São conhecidos por todos os valores de $g$ e $h$.
$x$ representa a informação original e $r$ um valor aleatório do commitment.

Considerando que os textos cifrados são publicamente armazenados, um verificador pode calcular $ cm = cm_1 \cdot cm_2 \cdot \cdot \cdot cm_n $ sem depender do provador e posteriormente verificar que uma soma $ s_x = \sum_{i=1}^{n}{x_i} $ enviada pelo provador é verdadeiro quando este também lhe enviar $ s_r = \sum_{i=1}^{n}{r_i} $ mantendo a igualdade:

$$ cm = g^{sx} h^{sr} = \prod_{i=1}^{n}{cm_i} $$

Já que:
$ cm = cm_1 \cdot cm_2 \cdot \cdot \cdot cm_n $
$ cm = ( g^{x_1} h^{r_1} )( g^{x_2} h^{r_2} ) \cdot \cdot \cdot ( g^{x_n} h^{r_n} ) $
$ cm = g^{x_1 + ... + x_n} h^{r_1 + ... + r_n} $
$ cm = g^{sx} h^{sr} $

---

### Esquema de criptografia com preservação de ordem

> A fazer
