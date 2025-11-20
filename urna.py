from os import system, name
import pickle # Aula 19-11-2025 Ciclo 4
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
# VARIÁVEIS GLOBAIS
# ==========================================================
candidatos = []
eleitores = []
eleitores_file = ""
candidatos_file = ""
titulos_computados = set() # guarda os titulos de eleitores que já votaram


# ==========================================================
# LER ARQUIVO DE CANDIDATOS
# ==========================================================
def ler_arquivo_candidatos():
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
                    continue # Depois daqui vai pra linha 54 (partes = linha.split(",")
                    
                partes = linha.split(",") # Divide a linha usando vírgula como delimitador, criando uma lista de partes.
                if len(partes) != 5: # 5 se refere aos campos: Nome, Numero, Partido, UF e Cargo
                    print(f"!!! Linha ignorada (formato inválido): {linha}") # Tem que ter exatamente 5 partes, senao: Messagem de Erro
                    continue
                    
                nome, numero, partido, uf, cargo = partes # Unpacking

                candidatos.append({
                    "nome": nome.strip(),
                    "numero": numero.strip(),
                    "partido": partido.strip(),
                    "uf": uf.strip().upper(),   # Padronizado em caixa alta para facilitar busca
                    "cargo": cargo.strip().upper()   # Padronizado em caixa alta para facilitar busca
                })
        limpar_tela()
        print(f"✔ Arquivo de candidatos carregado com sucesso!\n(Com um total de {len(candidatos)} candidatos)\n")
        time.sleep(2) # Aguarda 3 segundos e retorna para tela principal

    except FileNotFoundError: 
        print(f"❌ Arquivo '{candidatos_file}' não encontrado.\n")
    except Exception as erro:
        print(f"❌ Erro ao ler o arquivo: {erro}\n") # Saída de Erro genérico, utilizando o Exception
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# INICIAR VOTAÇÃO
# ==========================================================
def iniciar_votacao():
    limpar_tela()
    if len(candidatos) == 0 or len(eleitores) == 0: # Para as duas Leituras. Atual é Teste de condição de leitura de candidatos somente.
        print("\n❌ Você deve carregar candidatos e eleitores antes de solicitar resultados.\n")
        time.sleep(3)
        input("\nPressione ENTER para retornar...")
        return
    limpar_tela()
    filtro_eleitores_uf = [] #filtra os eleitores pela UF
    filtro_candidatos_uf = [] #Filtra os candidatos pela UF
    filtro_presidente = [] #filtra os candidatos a presidente da republica
    try:
        uf_urna = input("Digite a UF da urna: ").strip().upper()
        if len(uf_urna) != 2:
            print("UF inválida.")
            input("\nENTER para retornar...")
            return
        
        for c in candidatos:
            cargo = str(c.get("cargo", "")).strip().upper()
            uf_candidatos = str(c.get("uf", "")).strip().upper()
            if cargo == "P":
                filtro_presidente.append(c)
            if uf_candidatos == uf_urna:
                filtro_candidatos_uf.append(c)
        
        for e in eleitores:
            uf_eleitores = str(e.get("uf")).strip().upper()
            if uf_eleitores == uf_urna:
                filtro_eleitores_uf.append(e)
        
        titulo_eleitor = input("Informe o Título de Eleitor: ").strip()
        if not titulo_eleitor:
            print("Título vazio. Operação cancelada.")
            input("\nENTER...")
            return
        
        if titulo_eleitor in titulos_computados:
            print("O usuário já votou.")
            input("\nENTER para retornar...")
            return

        eleitor_encontrado = None
        for e in filtro_eleitores_uf:
            if str(e.get("titulo", "")).strip() == titulo_eleitor:
                eleitor_encontrado = e
                break
        

        if eleitor_encontrado:
            print(f"Eleitor: {eleitor_encontrado.get('nome','<sem nome>')}")
            print(f"Estado: {eleitor_encontrado.get('uf')}")
            
            
            # IMPLEMENTAR AQUI O RESTO DA FUNÇÃO #

        else:
            print("Eleitor não encontrado na UF.")
        input("\nPressione ENTER para retornar...")
        return
        
    except Exception as e:
        print(e)

# ==========================================================
# APURAÇÃO DOS VOTOS
# ==========================================================
def apurar_votos():
    limpar_tela()
    if len(candidatos) == 0 or len(eleitores) == 0:#Para as duas Leituras. Atual é Teste de condição de leitura de candidatos somente.
        print("\n❌ Você deve carregar candidatos e eleitores antes de solicitar apuração de votos.\n")
        time.sleep(3)
        input("\nPressione ENTER para retornar...")
        return
    limpar_tela()



    """Aqui deve constar o algoritmo de apuracao_votos()"""
    print("Se você está vendo esta tela, \nsignifica que os arquivos foram lidos e esta função está funcionando corretamente.")
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# LER ARQUIVO DE ELEITORES
# ==========================================================
def ler_arquivos_eleitores():
    limpar_tela()
    global eleitores, eleitores_file
    eleitores = []

    eleitores_file = input("Digite o nome do arquivo de eleitores (eleitores.txt): ").strip()
    if not eleitores_file:
        eleitores_file = "eleitores.txt"
    
    try:
        with open(eleitores_file ,"r", encoding= "utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue

                partes = linha.split(",")
                if len(partes) !=5:
                    print(f"!!! Linha ignorada (formato inválido): {linha}")
                    continue

                nome, rg, titulo, municipio, uf = partes

                eleitores.append({
                    "nome": nome.strip(),
                    "rg": rg.strip(),
                    "titulo": titulo.strip(),
                    "municipio": municipio.strip().upper(),
                    "uf": uf.strip().upper()
                })
        limpar_tela()
        print(f"✔ Arquivo de eleitores carregado com sucesso!\n(Com um total de {len(eleitores)} eleitores)\n")
        time.sleep(2)
    except FileNotFoundError: 
        print(f"❌ Arquivo '{eleitores_file}' não encontrado.\n")
    except Exception as erro:
        print(f"❌ Erro ao ler o arquivo: {erro}\n") 
    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# MOSTRAR RESULTADOS + BOLETIM
# ==========================================================
def mostrar_resultado():
    limpar_tela()
    if len(candidatos) == 0: # [ if len(candidatos) == 0 or len(eleitores) == 0 ] Para as duas Leituras. Atual é Teste de condição de leitura de candidatos somente.
        print("\n❌ Você deve carregar candidatos e eleitores antes de solicitar resultados.\n")
        time.sleep(3)
        input("\nPressione ENTER para retornar...")
        return
    limpar_tela()
    """Aqui deve constar o algoritmo de mostrar_resultados()"""
    print("Se você está vendo esta tela, \nsignifica que os arquivos foram lidos e esta função está funcionando corretamente.")
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
        print("=" * 38)
        try:
            opcaoMenu = int(input("Digite a opção desejada: "))
            match opcaoMenu:
                case 1:
                    ler_arquivo_candidatos()
                case 2:
                    ler_arquivos_eleitores()
                case 3:
                    iniciar_votacao()#EM TESTE
                case 4:
                    apurar_votos()#FALTA IMPLEMENTAR
                case 5:
                    mostrar_resultado()#FALTA IMPLEMENTAR
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

