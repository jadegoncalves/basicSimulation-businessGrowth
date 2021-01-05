# simulacao-empresa
 Simulação basica de crescimento de empresa 

# dados <br/>
margem de contribuição = ganho - custo fixo - custo variavel <br/>
lucro = margem de contribuição - investimento <br/>

Empresa:
investimento inicial: (>R$10000)<br/>
salario inicial: (R$1000 - R$2000)<br/>
custo fixo: (>R$2000)<br/>
custo unitário: (>R$100)<br/>
demanda: (100 p/ mes)<br/>
margem = (>100%)<br/>

produtividade total: multiplicação das produtividades dos funcionários diretos<br/>
produção: demanda * produtividade<br/>
custo variável: custo unitário * producao<br/>
preço = (custo fixo + custo variavel) * margem<br/>
ganho = preço * producao <br/>

#### funcionarios: 

salário: (começa com salario incial)

idade: incrementa todo ano

	- > 25 aumento de 25%
	- > 30 aumento de 30%
	- > 40 aumento de 40%
	- > 50 aposenta
	
satisfação: (começa com 50)

	- aumenta ou diminui aleatoriamente cada ano
	
produtividade: (começa com 100)

diretos: 

	- podem ser reduzidos a partir do investimento
	- satisfação baixa: < produtividade

indiretos:

	- recebem promoção
	- satisfação = 0: sai da empresa
	
