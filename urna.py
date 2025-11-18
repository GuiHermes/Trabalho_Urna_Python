from os import system, name
import time

"""
=============================================
# Trabalho Final - Urna Eletrônica
=============================================
Unilavras - 2025
=============================================
"""


# ==========================================================
# LIMPAR TELA
# ==========================================================
def limpar_tela():
    if name == 'nt':  # Windows
        system('cls')
    else:  # Linux / Mac
        system('clear')

limpar_tela()


# ==========================================================
# LER ARQUIVO DE CANDIDATOS
# ==========================================================
def lerArquivoCandidato():
    limpar_tela()
    global candidatos, candidatos_file
    candidatos = [] # Resetar os candidatos, para fazer uma nova leitura

    candidatos_file = input("Digite o nome do arquivo de Candidatos (candidatos.txt): ").strip()
    if not candidatos_file: # Verifica se candidatos_file está vazio (usuário pressionou Enter sem digitar nada)
        candidatos_file = "candidatos.txt" # Se estiver vazio, define o nome padrão "candidatos.txt"(Segue depois de ter apertado ENTER)

    try:
        with open(candidatos_file, "r", encoding="utf-8") as arq: # Formatação padrão UTF-8, padronizada para leitura interna do arquivo
            for linha in arq: # "Linha por linha, faça o seguinte: "
                linha = linha.strip() # strip para dividir em partes iguais, removendo os espaços
                if not linha: # Se a linha estiver agora vazia, prossiga.
                    continue # Depois daqui vai pra linha 44 (partes = linha.split(",")
                    
                partes = linha.split(",") # Divide a linha usando vírgula como delimitador, criando uma lista de partes.
                if len(partes) != 5: # 5 se refere aos campos: Nome, Numero, Partido, UF e Cargo
                    print(f"!!! Linha ignorada (formato inválido): {linha}") # Tem que ter exatamente 5 partes, senao: Messagem de Erro
                    continue
                    
                nome, numero, partido, estado, cargo = partes # Unpacking

                candidatos.append({
                    "nome": nome.strip(),
                    "numero": numero.strip(),
                    "partido": partido.strip(),
                    "estado": estado.strip().upper(),   # Padronizado em caixa alta para facilitar busca
                    "cargo": cargo.strip().upper()   # Padronizado em caixa alta para facilitar busca
                })
        limpar_tela()
        print(f"✔ Arquivo de candidatos carregado com sucesso!\n(Com um total de {len(candidatos)} candidatos)\n")
        time.sleep(3) # Aguarda 3 segundos e retorna para tela principal

    except FileNotFoundError: 
        print(f"❌ Arquivo '{candidatos_file}' não encontrado.\n")
    except Exception as erro:
        print(f"❌ Erro ao ler o arquivo: {erro}\n") # Saída de Erro genérico, utilizando o Exception


# ==========================================================
# INICIAR VOTAÇÃO
# ==========================================================
def iniciarVotacao():
    limpar_tela()
    """Aqui deve constar o algoritmo de votação"""
    print("Aqui deve constar o algoritmo de iniciarVotacao()")
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# APURAÇÃO DOS VOTOS
# ==========================================================
def ApuracaoVotos():
    limpar_tela()
    """Aqui deve constar o algoritmo de apuracao_votos()"""
    print("Aqui deve constar o algoritmo de ApuracaoVotos()")
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# LER ARQUIVO DE ELEITORES
# ==========================================================
def lerArquivoEleitores():
    limpar_tela()
    """Aqui deve constar o algoritmo de lerArquivoEleitores()"""
    print("Aqui deve constar o algoritmo de lerArquivoEleitores()")
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# MOSTRAR RESULTADOS + BOLETIM
# ==========================================================
def MostrarResultados():
    limpar_tela()
    """Aqui deve constar o algoritmo de mostrar_resultados()"""
    print("Aqui deve constar o algoritmo de MostrarResultados()")
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# MENU PRINCIPAL
# ==========================================================
def menu():
    global candidatos_file, eleitores_file, candidatos, eleitores
    while True:
        limpar_tela() 
        print("\n" + "=" * 10 + "[ MENU PRINCIPAL ]" + "=" * 10)
        print("1 - Selecionar arquivo de Candidatos")
        print("2 - Selecionar arquivo de Eleitores")
        print("3 - Iniciar votação")
        print("4 - Apurar votos")
        print("5 - Mostrar resultados")
        print("6 - Fechar programa")
        print("=" * 39)
        try:
            opcaoMenu = int(input("Digite a opção desejada: "))
            match opcaoMenu:
                case 1:
                    lerArquivoCandidato()
                case 2:
                    lerArquivoEleitores()#FALTA IMPLEMENTAR
                case 3:
                    iniciarVotacao()#FALTA IMPLEMENTAR
                case 4:
                    ApuracaoVotos()#FALTA IMPLEMENTAR
                case 5:
                    MostrarResultados()#FALTA IMPLEMENTAR
                case 6:
                    limpar_tela()
                    print("\nEncerrando sistema...")
                    time.sleep(1)
                    print("✅ Sistema encerrado com sucesso!")
                    break
                case _:
                    input("Opção inválida, digite uma opção válida!")
                    limpar_tela()
        except ValueError:
            print(f"Digite uma opção válida!")


# ==========================================================
# INICIAR SISTEMA
# ==========================================================
if __name__ == "__main__":
    menu()
