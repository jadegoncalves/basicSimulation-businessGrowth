import random
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import statistics

investimento_inicial = 10000.00     # qual investimento inicial na empresa
porcento_investimento = 30          # quanto da margem vai investir (porcentagem)
salario_inicial = 1000.00           # quanto cada funcionario irá receber de salário inicialmente
sub_custo_fixo = 2000.00            # custo fixo de luz, água, condomínio
custo_unitario = 100.00             # quanto custa produzir UM produto
demanda = 200                       # quantas peças serão produzidas mensalmente
cadencia_por_pessoa = 50            # quantas peças cada pessoa consegue produzir
margem = 200                        # quantos % do custo para preço de venda
carteira_inicial = 0.01             # com quantos reais a empresa irá começar
probabilidade_satisfacao = 70       # probabilidade de satisfação dos funcionários em relação a empresa
probabilidade_produtividade = 90    # probabilidade de contratação de alguém apto
probabilidade_altera_demanda = 20   # probabilidade de aumentar ou diminuir a demanda da produção
periodo_simulacao = 20              # tempo de simulacao em anos

class Empresa:

    def __init__(self):
        self.carteira = carteira_inicial
        self.investimento = investimento_inicial
        self.carteiraTotal = self.carteira + self.investimento
        self.dicionarioFuncionarios = []
        self.receitas = []
        self.periodo = []
        self.mes = 1 # TEMPORARIO RETIRAR

    def alteraStatusFuncionariosMassa(self, contrata = True):

        i = len(self.dicionarioFuncionarios)
        quantidade = round(demanda / cadencia_por_pessoa)

        while (i < quantidade):
            self.dicionarioFuncionarios.append(Funcionario(salario_inicial))
            i += 1
      
        while (i > quantidade):
            rand = random.randint(0, len(self.dicionarioFuncionarios) - 1)
            self.dicionarioFuncionarios.pop(rand)
            i -= 1


    def calculaGastos(self):
        produtividade_total = 1
        sub_custo_funcionario = 0

        if(len(self.dicionarioFuncionarios) > 0):
            for funcionario in self.dicionarioFuncionarios:
                produtividade_total = produtividade_total * \
                    (funcionario.produtividade/100)
                sub_custo_funcionario = sub_custo_funcionario + funcionario.salario
        else:
            produtividade_total = 0
            sub_custo_funcionario = 0.00

        self.produtividade = "%.2f" % (produtividade_total * 100)
        self.producao = demanda * produtividade_total
        self.custo_variavel = custo_unitario * self.producao
        self.custo_fixo = sub_custo_fixo + sub_custo_funcionario

    def calculaGanho(self):
        preco = ((margem / 100) + 1) * custo_unitario
        self.ganho = preco * self.producao

    def realizaPagamento(self):
        margem_de_contribuicao = self.ganho - self.custo_variavel - self.custo_fixo
        if (margem_de_contribuicao < 0):
            self.investimento = self.investimento + margem_de_contribuicao
            margem_de_contribuicao = 0
        lucro = margem_de_contribuicao * (1 - (porcento_investimento/100))
        self.carteira = self.carteira + lucro
        self.investimento = self.investimento + (margem_de_contribuicao - lucro)
        self.carteiraTotal = self.carteira + self.investimento

    def updateAnual(self):

        for mes in range(1, 13):
            self.calculaGastos()
            self.calculaGanho()
            self.realizaPagamento()
            self.periodo.append(self.mes)
            self.receitas.append(self.carteiraTotal)
            self.updateFuncionarios("mensal")
            if(self.alteraDemanda()):
                self.alteraStatusFuncionariosMassa()

            self.mes += 1
    
    def updateFuncionarios(self, time = "mensal"):

        for funcionario in self.dicionarioFuncionarios:
            if (time == "anual"):
                funcionario.updateAnual()
            else:
                feedback = funcionario.updateMensal()
                if(feedback <= 0):
                    self.demiteFuncionario(funcionario)

    def demiteFuncionario(self, funcionario):

        self.dicionarioFuncionarios.remove(funcionario)
        self.alteraStatusFuncionariosMassa()
        
    def alteraDemanda(self):
        demandaAlterada = False
        global demanda
        desvioPadraoEntregas = statistics.pvariance(self.receitas)

        # Aumento por boas práticas
        if(desvioPadraoEntregas < (0.1*demanda)):
            rand = random.randint(10,100)
            demanda = round(demanda * (1 + (rand/100)))
            demandaAlterada = True
        else:
            # o que posso fazer se não atinjo a meta... hum..
            pass
        
        # Aumento por probabilidade
        rand = random.randint(0,100)
        if(rand >= (100 - probabilidade_altera_demanda)):
            randAlteracao = random.randint(2,6)

            if (rand >= 5):
                demanda = round(demanda * (1 + (randAlteracao/100)))
            else:
                demanda = round(demanda * (1 - (randAlteracao/100)))
            
            demandaAlterada = True

        return demandaAlterada

    def reset(self):
        self.carteira = 0.01
        self.investimento = investimento_inicial

    def __str__(self):
        string = "Carteira total: " + ("%.2f" % self.carteiraTotal)
        string = string + "\r\nInvestimento total: " + \
            ("%.2f" % self.investimento)
        string = string + "\r\nProdutividade: " + str(self.produtividade) + "%"
        string = string + "\r\nQuantidade Funcionários: " + str(len(self.dicionarioFuncionarios))
        if(len(self.dicionarioFuncionarios) > 0):
            mediaSatisfacao = 1
            for funcionario in self.dicionarioFuncionarios:
                mediaSatisfacao = mediaSatisfacao * (funcionario.satisfacao / 100)
        else:
            mediaSatisfacao = 0
        
        string = string + "\r\nMedia Satisfação dos funcionarios: " + ( "%.2f" % (mediaSatisfacao*100))

        return string


class Funcionario:

    def __init__(self, salario):
        self.salario = salario_inicial

        rand = random.randint(0, 100)

        if rand < 60:
            self.tipo = "Direto"
        else:
            self.tipo = "Indireto"

        if(rand >= (100 - probabilidade_produtividade)):
            self.produtividade = 100
        else:
            self.produtividade = rand + 10

        self.idade = 18
        self.satisfacao = 100

    def aumentaSalario(self):
        if(self.idade % 5 == 0):
            self.salario = self.salario * (1 + (self.idade/100))

    def modificaProdutividade(self, aumenta):
        if(aumenta == 1):
            if self.produtividade < 100:
                self.produtividade += 10
        else:
            if self.produtividade > 0:
                self.produtividade -= 10

    def modificaSatisfacao(self, aumenta):
        if(aumenta == 1):
            if self.satisfacao < 100:
                self.satisfacao += 1
        else:
            if self.satisfacao > 0:
                self.satisfacao -= 1

        if(self.tipo == "Direto"):
            self.modificaProdutividade(aumenta)

        return self.satisfacao

    def updateAnual(self):
        self.idade += 1
        if(self.tipo == "Indireto"):
            self.aumentaSalario()

    def updateMensal(self):
        rand = random.randint(0, 100)
        if (rand >= (100 - probabilidade_satisfacao)):
            aumenta = 1
        else:
            aumenta = 0

        return self.modificaSatisfacao(aumenta)

    def __str__(self):
        return ("Salário: " + str(self.salario) +
        "\r\nIdade: " + str(self.idade) + 
        "\r\nProdutividade: " + str(self.produtividade) + 
        "\r\nSatisfação: " + str(self.satisfacao) +
        "\r\nTipo: " + self.tipo) 

class Grafico:

    def __init__(self, objeto):
        self.xData = []
        self.yData = []
        self.dados = objeto

    def animate(self,i):

        self.yData.append(self.dados.receitas[i])
        self.xData.append(self.dados.periodo[i])

        self.graph.set_data(self.xData, self.yData)

        return self.graph,

    def desenha_grafico(self):

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.2, bottom=0.35)

        self.graph, = ax.plot([], [])
        
        plt.title("Simple Business Case Simulator")
        plt.xlabel('time (m)')
        plt.ylabel('revenue (R$)')

        ax.set_xlim(0, (len(self.dados.periodo) - 1))
        ax.set_ylim(min(self.dados.receitas), max(self.dados.receitas))

        ani = animation.FuncAnimation(fig, self.animate,
        interval=20, blit=True, repeat= False, frames=(len(self.dados.receitas)-1))

        plt.show()  # melhorar visualização do grafico

if __name__ == "__main__":

    simulaEmpresa = Empresa()
    simulaEmpresa.alteraStatusFuncionariosMassa()
    arq = open('log.txt', 'w')
    escreverLog = ""

    for ano in range(0, periodo_simulacao):

        inicial = simulaEmpresa.carteiraTotal

        simulaEmpresa.updateAnual()
        simulaEmpresa.updateFuncionarios("anual")

        final = simulaEmpresa.carteiraTotal
        crescimento = "%.2f" % (((final - inicial)/abs(inicial)) *100)
        print("Crescimento de: " + crescimento + "%")
        escreverLog = escreverLog + "Crescimento de: " + crescimento + "%\r\n"        
    
    print("Resultado Empresa:")
    print(simulaEmpresa)
    print("Último Crescimento: " + crescimento + "%")

    graph = Grafico(simulaEmpresa)
    graph.desenha_grafico()

    escreverLog = escreverLog + "Resultado Empresa:\r\n"
    escreverLog = escreverLog + str(simulaEmpresa)
    escreverLog = escreverLog + "\r\nÚltimo Crescimento: " + crescimento + "%"

    arq.write(escreverLog)
    arq.close()