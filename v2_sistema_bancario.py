import textwrap #FORMATAÇÕES DE TEXTO E SAÍDA DO TERMINAL
import datetime
from datetime import  date, datetime, time, timedelta

def menu():
    menu = f"""
    ==================================================
    Digite a opção da operação desejada

    [d]\tDepositar
    [s]\tSacar
    [e]\tVisualizar extrato
    [c]\tCriar usuário
    [l]\tListar contas
    [cc]\tCriar conta-corrente
    [q]\tSair
    
    """
    return input(textwrap.dedent(menu)) # RETORNA O MENU FORMATADO COM IDENTAÇÃO DO LADO ESQUERDO DA TELA E COM TAB ATIVADO

def saque(*, saldo, extrato, valor_saque, valor_saque_unitario, numero_saques_dia, limite_saques, mascara_ptbr, date_list):
    limite_liberado = numero_saques_dia <= limite_saques
    saque_liberado = valor_saque <= valor_saque_unitario and valor_saque > 0
    saldo_positivo = valor_saque <= saldo 

    if limite_liberado:
        if saque_liberado:
            if saldo_positivo:
                data_transacao = datetime.now()
                data_formatada = data_transacao.strftime(mascara_ptbr)
                date_list.append(data_transacao)

                extrato += textwrap.dedent(f"| Data e hora da movimentação: {data_formatada}| Valor sacado:\tR$ {valor_saque:.2f}\t |\n")

                saldo -= valor_saque

                numero_saques_dia += 1

                print("Valor sacado com sucesso!")
            else:
                print("** NÃO É POSSÍVEL SACAR O DINHEIRO, POR FALTA DE SALDO. **")
        else:
            print("**O VALOR DE SAQUE SOLICITADO NÃO SE ENQUADRA NO LIMITE PERMITIDO: 'ENTRE R$ 1.00 E R$ 500.00'**")
    else:
        limite_atingido = date_list[0]
        contagem_dia = limite_atingido + timedelta(days=1)
        data_convertida = datetime.strftime(contagem_dia, mascara_ptbr)
        print(f"""
        --------------------------------------------------
        **  VOCÊ ATINGIU O LIMITE DE SAQUES DIÁRIOS.  **
                    POR FAVOR, VOLTE AMANHÃ!
        --------------------------------------------------
        Seu limite será liberado em: {data_convertida}                      
            """)
        
    return saldo, extrato, numero_saques_dia

def depositar(saldo, extrato, date_list, valor_deposito, mascara_ptbr, /):
    valor_positivo = valor_deposito > 0

    if valor_positivo:
        #REGISTRANDO A DATA DA MOVIMENTAÇÃO
        data_transacao = datetime.now()
        data_formatada = data_transacao.strftime(mascara_ptbr)
        date_list.append(data_transacao)
        extrato += textwrap.dedent(f"| Data e hora da movimentação: {data_formatada}| Valor depositado:\tR$ {valor_deposito:.2f}\t |\n")
        
        saldo += valor_deposito

        print("=" *50)
        print("Valor depositado com sucesso!")
    else:
        print("=" *50)
        print("**O valor informado é inválido, insira um valor maior que R$ 1.00*")
    
    return saldo, extrato, date_list
    
def criar_usuario(usuarios):
    cpf = input("Informe seu CPF, somente números: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("=" *50)
        print("X X X Já existe usuário com este CPF! X X X")
        return
    
    #Coletando os dados do usuário se a condição do 'if usuario' não existir (for False)
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro - n° - bairro - cidade/sigla Estado(UF)): ")

    #Fazemos um 'append' para dentro da lista criando um dicionário desse novo usuário
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    
    print("=" *50)    
    print("\o/ \o/ \o/ Usuário criado com sucesso! \o/ \o/ \o/")

    return usuario

def listar_contas(contas):
    if contas == []:
        print("=" *50)
        print(" - - - AINDA NÃO HÁ CONTAS CADASTRADAS, EXPERIMENTE CRIAR UMA CONTA E VOLTE AQUI - - - ")
    else:
        # A variável 'conta' percorre a variável 'contas' que armazena toda lista de contas passada no parâmetro 'contas'.
        for conta in contas: #Formatando a saída
            conta_usuario = f"""
            Titular: {conta['usuario']['nome']}
            Agência: {conta['agencia']}
            Conta: {conta['numero_conta']}
            """
            print("=" * 50)
            print(textwrap.dedent(conta_usuario))
    
def criar_conta_corrente(agencia, numero_conta, lista_usuarios, lista_contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, lista_usuarios)

    if usuario:
        print("=" *50)
        print("\n\`'´/ Conta criada com sucesso! \`'´/")
        salvar_conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        return lista_contas.append(salvar_conta)

    print("\nX X X Usuário não encontrado, fluxo de criação de conta encerrado! X X X")

def filtrar_usuario(cpf, lista_usuarios):
    usuarios_filtrados = [
                        usuario #cria uma variável com qualquer nome para armazenar o resultado das iterações
                        for usuario in lista_usuarios #fazemos a iteração dentro da lista de usuários para verificar se existe algum dado igual ao informado
                            if usuario["cpf"] == cpf #fazemos a verificação da condição se o cpf encontrado é igual ao informado.
                        ]
    return usuarios_filtrados[0] if usuarios_filtrados else None #retornamos o primeiro usuário encontrado 'se' o filtro for True, senão (else) retorna 'None'

def funcao_extrato(saldo, /, *, extrato):
    if extrato == "":
        extrato = print("""
---------------------------------------------                  
            **  EXTRATO  **
---------------------------------------------
    * Não foram realizadas movimentações *
            """)
    else:
        extrato = print(f"""
-------------------------------------------
                SALDO
-------------------------------------------
Seu saldo atual é de: R$ {saldo:.2f}
-------------------------------------------                  
                EXTRATO
-------------------------------------------
Histórico de transações:\n{extrato}

    """)
    return extrato


def main():

    #VARIÁVEIS E VALORES FIXOS (REGRAS DE NEGÓCIO)
    saldo = 5000
    valor_saque_unitario = 3000
    numero_saques_dia = 1 # Se o n° saques inicia com '0' esta é uma transação disponível (para 3 transações diárias = 0, 1 e 2), portanto o LIMITE_SAQUES DEVE SER FIXADO EM '2'
    LIMITES_SAQUES = 4  #independentemente do tipo de movimentação (depósito/saque)
    AGENCIA = "0001"

    #REGISTROS E LOG DE MOVIMENTAÇÕES
    extrato = ""
    date_list = [] #FORMATO: [{"dd/mm/yyyy hh:mm:ss", "dd/mm/yyyy hh:mm:ss", ...}]
    lista_contas = [] # FORMATO: [{"agencia": "0001", "numero_conta": "numero_conta", "usuario": "nome_do_usuario_ou_titular"}]
    lista_usuarios = [] # FORMATO: [{"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco}]

    #FORMATOS DE DATAS E HORAS
    mascara_ptbr = "%d/%m/%Y %H:%M:%S"
    
    while True:

        opcao = menu()

        if opcao == "d":
            valor_deposito = float(input("Informe o valor que deseja depositar: "))
            
            saldo, extrato, date_list = depositar(
                saldo,
                extrato,
                date_list,
                valor_deposito,
                mascara_ptbr
            )
        elif opcao == "s":

            valor_saque = float(input("Informe o valor que deseja sacar: "))

            saldo, extrato, numero_saques_dia = saque(
                saldo=saldo,
                extrato=extrato,
                valor_saque=valor_saque,
                valor_saque_unitario=valor_saque_unitario,
                numero_saques_dia=numero_saques_dia,
                limite_saques=LIMITES_SAQUES,
                mascara_ptbr=mascara_ptbr,
                date_list=date_list
            )

        elif opcao == "e":

            funcao_extrato(
                saldo,
                extrato=extrato
            )
        
        elif opcao == "c":
            criar_usuario(lista_usuarios)

        elif opcao == "l":
            listar_contas(lista_contas)

        elif opcao == "cc":
            numero_conta = len(lista_contas) + 1 #PARA CADA VEZ QUE A OPERAÇÃO É CHAMADA, LISTA CONTAS SOMA UMA UNIDADE A CADA CONTA NOVA PARA GERAR UM NOVO N° DE CONTA.
            criar_conta_corrente(AGENCIA, numero_conta, lista_usuarios, lista_contas) #A FUNÇÃO JÁ RETORNA A CONTA SALVA NA LISTA DE CONTAS.
            
        elif opcao == "q":
            print("""
                ___________________________________________
                
                OBRIGADO POR USAR NOSSO SERVIÇO, ATÉ BREVE.

                SAINDO...
                ___________________________________________
                """)
            break
        else :
            print("""
                    Operação inválida!
                    Por favor, selecione novamente a operação desejada.
                """)

main()