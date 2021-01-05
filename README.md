# simulacao-empresa
 Simulação basica de crescimento de empresa 

## Dados <br/>
### Empresa:

**margem de contribuição** = ganho - custo fixo - custo variavel <br/>
**lucro** = margem de contribuição - investimento <br/>
**investimento inicial**: (>R$10000)<br/>
**salário inicial**: (R$1000 - R$2000)<br/>
**custo fixo**: (>R$2000)<br/>
**custo unitário**: (>R$100)<br/>
**demanda**: (100 p/ mes)<br/>
**margem** = (>100%)<br/>

**produtividade total**: multiplicação das produtividades dos funcionários diretos<br/>
**produção**: demanda * produtividade<br/>
**custo variável**: custo unitário * producao<br/>
**preço** = (custo fixo + custo variavel) * margem<br/>
**ganho** = preço * producao <br/>

### Funcionários: 

**salário:** (começa com salario incial)<br/>
**idade:** incrementa todo ano

	- > 25 aumento de 25%
	- > 30 aumento de 30%
	- > 40 aumento de 40%
	- > 50 aposenta
	
**satisfação:** (começa com 50)

	- aumenta ou diminui aleatoriamente cada ano
	
**produtividade:** (começa com 100)<br/>
**diretos:** 

	- podem ser reduzidos a partir do investimento
	- satisfação baixa: < produtividade

**indiretos:**

	- recebem promoção
	- satisfação = 0: sai da empresa
	
### Bibliografia
https://towardsdatascience.com/12-data-science-projects-for-12-days-of-christmas-aff693f5ed2b
random
matplotlib
