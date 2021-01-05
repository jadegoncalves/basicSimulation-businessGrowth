import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

investimento_inicial = 10000.00     # qual investimento inicial na empresa
porcento_investimento = 0           # quanto da margem vai investir (porcentagem)
salario_inicial = 1000.00           # quanto cada funcionario irá receber de salário inicialmente
sub_custo_fixo = 2000.00            # custo fixo de luz, água, condomínio
custo_unitario = 100.00             # quanto custa produzir UM produto
demanda = 100                       # quantas peças eu tenho que produzir mensalmente
margem = 200                        # quantos % do custo para preço de venda
carteira_total = 0.01               # com quantos reais a empresa irá começar
probabilidade_satisfacao = 70       # probabilidade de satisfação dos funcionários em relação a empresa

class Empresa:

    def __init__(self):
        self.carteiraTotal = carteira_total
        self.investimento = investimento_inicial
        self.dicionarioFuncionarios = []

    def contrataFuncionario(self):
        quantidade = 5  

        for p in range(0, quantidade):
            self.dicionarioFuncionarios.append(Funcionario(salario_inicial))

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
        self.carteiraTotal = self.carteiraTotal + lucro
        self.investimento = self.investimento + \
            (margem_de_contribuicao - lucro)

    def demiteFuncionario(self, funcionario):
        self.dicionarioFuncionarios.remove(funcionario)

    def reset(self):
        self.carteiraTotal = 0.01
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
        self.produtividade = 100
        self.idade = 18
        self.satisfacao = 50
        rand = random.randint(0, 100)
        if rand < 60:
            self.tipo = "Direto"
        else:
            self.tipo = "Indireto"

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
            self.satisfacao += 10
        else:
            self.satisfacao -= 10

        if(self.tipo == "Direto"):
            self.modificaProdutividade(aumenta)

        return self.satisfacao

    def updateAnual(self):
        self.idade += 1
        if(self.tipo == "Indireto"):
            self.aumentaSalario()

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


def update():

    meses = [0]
    #simulaEmpresa.reset()
    receitas = [simulaEmpresa.carteiraTotal]

    for mes in range(1, 13):
        simulaEmpresa.calculaGastos()
        simulaEmpresa.calculaGanho()
        simulaEmpresa.realizaPagamento()
        meses.append(mes)
        receitas.append(simulaEmpresa.carteiraTotal)
        #print("MES: " + str(mes))
        #print(simulaEmpresa)

    return meses, receitas


def updateFuncionarios():

    for funcionario in simulaEmpresa.dicionarioFuncionarios:
        feedback = funcionario.updateAnual()
        #print(funcionario)
        if(feedback <= 0):
            simulaEmpresa.demiteFuncionario(funcionario)


def updateGrafico(val):
    global custo_unitario, margem, demanda
    custo_unitario = scusto.val
    margem = smargem.val
    demanda = sdemanda.val
    # melhorar update do gráfico
    #meses, receitas = update()
    #graph.set_ydata(receitas)
    #fig.canvas.draw_idle()


if __name__ == "__main__":

    simulaEmpresa = Empresa()
    simulaEmpresa.contrataFuncionario()
    arq = open('log.txt', 'w')
    escreverLog = ""

    for ano in range(0, 10):

        print("ANO " + str(ano))
        inicial = simulaEmpresa.carteiraTotal
        meses, receitas = update()

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        graph, = plt.plot(meses, receitas)
        plt.title("ANO 202" + str(ano))

        axcolor = 'lightgoldenrodyellow'
        axcusto = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        axmargem = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        axdemanda = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)

        scusto = Slider(axcusto, 'Custo', 1, 200, valinit=custo_unitario)
        smargem = Slider(axmargem, 'Margem', 100, 500, valinit=margem, valstep=5)
        sdemanda = Slider(axdemanda, 'Demanda', 10, 1000, valinit=demanda)

        scusto.on_changed(updateGrafico)
        smargem.on_changed(updateGrafico)
        sdemanda.on_changed(updateGrafico)

        final = simulaEmpresa.carteiraTotal
        crescimento = "%.2f" % (((final - inicial)/inicial) *100)
        print("Crescimento de: " + crescimento + "%")
        escreverLog = escreverLog + "Crescimento de: " + crescimento + "%\r\n"
        updateFuncionarios()
        
        plt.show()  # melhorar visualização do grafico
    
    print("Resultado Empresa:")
    print(simulaEmpresa)
    print("Último Crescimento: " + crescimento + "%")

    escreverLog = escreverLog + "Resultado Empresa:\r\n"
    escreverLog = escreverLog + str(simulaEmpresa)
    escreverLog = escreverLog + "\r\nÚltimo Crescimento: " + crescimento + "%"

    arq.write(escreverLog)
    arq.close()