def lerArquivoCandidato(): #FALTA IMPLEMENTAR
    global candidatos, candidatos_file
    candidatos =[]
    candidatos_file = input("Digite o nome do arquivo de Candidatos (candidatos.txt): ")
    candidatos_file = f"./{candidatos_file}"
    try:
        print("FALTA IMPLEMENTAR")
             

    except Exception as e:
        print(f"Erro ao ler o arquivo. {e}\nSelecione novamente.")

def lerArquivoEleitores(): #FALTA IMPLEMENTAR
    global eleitores, eleitores_file
    eleitores = []
    eleitores_file = input("Digite o nome do arquivo de Eleitores (eleitores.txt): ")
    try:
        print("#FALTA IMPLEMENTAR")
            
    except FileNotFoundError:
        print(f"Arquivo {eleitores_file} não encontrado.\nSelecione novamente.")

def iniciarVotacao():#FALTA IMPLEMENTAR
    print(f"Ainda falta implementar")
            
def menu(): 
    global candidatos_file, eleitores_file, candidatos, eleitores
    while True:
        print("_____ URNA ELETRONICA _____")
        print("1 - Selecionar arquivo de Candidatos")
        print("2 - Selecionar arquivo de Eleitores")
        print("3 - Iniciar votação")
        print("4 - Apurar votos")
        print("5 - Mostrar resultados")
        print("6 - Fechar programa")
        try:
            opcaoMenu = int(input("Digite a opção desejada: "))
            match opcaoMenu:
                case 1:
                    lerArquivoCandidato()#FALTA IMPLEMENTAR
                case 2:
                    lerArquivoEleitores()#FALTA IMPLEMENTAR
                case 3:
                    iniciarVotacao()#FALTA IMPLEMENTAR
                case 4:
                    print("Falta implementar")#FALTA IMPLEMENTAR
                case 5:
                    print("Falta implementar")#FALTA IMPLEMENTAR
                case 6:
                    print("Obrigado por usar o nosso programa!")
                    break
                case _:
                    print("Opção inválida, digite uma opção válida!")
        except ValueError:
            print(f"Digite uma opção válida!")

menu()
