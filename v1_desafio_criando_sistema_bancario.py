saldo = 0
limite_deposito = 500
limite_saque_unitario = 500
limite_diario = 3
numero_saque = 0
LIMITES_SAQUES = 3
extrato = ""

menu = f"""
    Digite a opção da operação desejada

    [s] - Sacar
    [d] - Depositar
    [e] - Visualizar extrato
    [q] - Sair
    
"""

while True:
    opcao = input(menu)

    if opcao == "s":
        valor_saque = float(input(f"""
            ___________________________________                    
            |     **  PAINEL DE SAQUE  **     |
            -----------------------------------
            Informe o valor que deseja sacar: 
            """))

        if numero_saque < LIMITES_SAQUES:
            if valor_saque <= limite_saque_unitario and valor_saque > 0:
                if saldo >= valor_saque:
                    extrato += (f"| Valor sacado:     R$ {valor_saque:.2f} |\n")

                    saldo -= valor_saque

                    print("Valor sacado com sucesso!")
                    numero_saque += 1

                else:
                    print("** NÃO É POSSÍVEL SACAR O DINHEIRO, POR FALTA DE SALDO. **")
            else:
                print("**O VALOR DE SAQUE SOLICITADO É MAIOR QUE QUE O LIMITE PERMITIDO 'R$ 500.00'**")
        else:
            print("""
            --------------------------------------------------
                **  VOCÊ ATINGIU O LIMITE DIÁRIO DE SAQUES.  **
                        POR FAVOR, VOLTE AMANHÃ!
            --------------------------------------------------                      
                """)

    elif opcao == "d":
        valor_deposito = float(input(f"""
            ______________________________________                    
            |     **  PAINEL DE DEPÓSITO  **     |
            --------------------------------------
            Informe o valor que deseja depositar: 
            """))
        
        if ((valor_deposito <= limite_deposito) and (valor_deposito > 0)):
            if limite_diario != 0:
                extrato += (f"| Valor depositado: R$ {valor_deposito:.2f} |\n")
                saldo += valor_deposito
        

                print("Valor depositado com sucesso!")

                limite_diario -= 1

            else:
                print("""
            --------------------------------------------------
            **  VOCÊ ATINGIU O LIMITE DIÁRIO DE DEPÓSITOS.  **
                        POR FAVOR, VOLTE AMANHÃ!
            --------------------------------------------------                      
                   """)

        else:
            print("**O valor não pôde ser depositado, o limite por depósito é de R$ 500.00**")

    elif opcao == "e":

        if extrato == "":
            print("""
            ---------------------------------------------                  
                        **  EXTRATO  **
            ---------------------------------------------
                * Não foram realizadas movimentações *
                  """)
        else:
            print(f"""
            -------------------------------------------                  
                            EXTRATO
            -------------------------------------------
                """)
            print(f"Histórico de transações:\n{extrato}")
            
        print(f"""
            -------------------------------------------
                            SALDO
            -------------------------------------------
                +  Seu saldo atual é de: R$ {saldo:.2f}
            -------------------------------------------
        """)
        
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