from os import system, name
import os # manipular caminhos de pasta
import pickle 
import time
from colorama import init, Fore, Style
import pygame # importei para a biblioteca de som
import matplotlib.pyplot as plt # importei para gráficos 
import random

init(autoreset=True)


"""
=============================================
# Trabalho Final - Urna Eletrônica
=============================================
Unilavras - 2025
=============================================
"""

# ==========================================================
#  = CONFIGURAÇÃO DE SOM
# ==========================================================
try:
    pygame.mixer.init() # Inicializa o mixer de som
except Exception as e:
    print(Fore.RED + f"Erro ao inicializar sistema de som: {e}")

def tocar_som(nome_arquivo):
    """
    Função auxiliar para tocar sons da pasta 'Sons'
    """
    caminho = os.path.join("Sons", nome_arquivo) # Cria o caminho Sons/arquivo.mp3
    try:
        if os.path.exists(caminho):
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()
        else:
            # um aviso se o arquivo não existir
            print(Fore.RED + f"(Audio não encontrado: {nome_arquivo})")
    except Exception as e:
        print(Fore.RED + f"Erro ao tocar audio: {e}")


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
# BOAS-VINDAS
# ==========================================================

def menu_boas_vindas():
    limpar_tela()
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + Style.BRIGHT + "       BEM-VINDO AO SISTEMA DE URNA ELETRÔNICA")
    print(Fore.CYAN + "=" * 50)
    print()
    print(Fore.YELLOW + "Projeto final – Estruturas de Dados – UNILAVRAS")
    print(Fore.YELLOW + "Desenvolvido por: Guilherme Hermes, Manuel Victor, Hian Oliveira, Matheus Rodrigues")
    print(Fore.CYAN + "-" * 50)
    print(Style.RESET_ALL)

    input(Fore.MAGENTA + "\nPressione ENTER para continuar..." + Style.RESET_ALL)
    
    limpar_tela()
    
# ==========================================================
# VARIÁVEIS GLOBAIS
# ==========================================================
candidatos = []
eleitores = []
eleitores_file = ""
candidatos_file = ""
titulos_computados = set() 
resultados_apurados = {} 
CARGOS_INFO = {
    "F": {"nome": "Deputado Federal", "digitos": 4},
    "E": {"nome": "Deputado Estadual", "digitos": 5},
    "S": {"nome": "Senador", "digitos": 3},
    "G": {"nome": "Governador", "digitos": 2},
    "P": {"nome": "Presidente", "digitos": 2},
}

# ==========================================================
# LER ARQUIVO DE CANDIDATOS
# ==========================================================
def ler_arquivo_candidatos():
    limpar_tela()
    global candidatos, candidatos_file
    candidatos = [] 

    candidatos_file = input("Digite o nome do arquivo de Candidatos (candidatos.txt): ").strip()
    if not candidatos_file: 
        candidatos_file = "candidatos.txt" 

    try:
        with open(candidatos_file, "r", encoding="utf-8") as arq: 
            for linha in arq: 
                linha = linha.strip() 
                if not linha: 
                    continue 
                    
                partes = linha.split(",") 
                if len(partes) != 5: 
                    print(f"!!! Linha ignorada (formato inválido): {linha}") 
                    continue
                    
                nome, numero, partido, uf, cargo = partes 

                candidatos.append({
                    "nome": nome.strip(),
                    "numero": numero.strip(),
                    "partido": partido.strip(),
                    "uf": uf.strip().upper(),   
                    "cargo": cargo.strip().upper()   
                })
        limpar_tela()
        print(f"✔ Arquivo de candidatos carregado com sucesso!\n(Com um total de {len(candidatos)} candidatos)\n")
        time.sleep(2) 

    except FileNotFoundError: 
        print(f"❌ Arquivo '{candidatos_file}' não encontrado.\n")
    except Exception as erro:
        print(f"❌ Erro ao ler o arquivo: {erro}\n") 
    input("\nPressione ENTER para retornar...")
    return

# ==========================================================
# INICIAR VOTAÇÃO
# ==========================================================
def iniciar_votacao():
    limpar_tela()
    
    # Parar o hino (ou qualquer música anterior) ao entrar na votação para não atrapalhar
    pygame.mixer.music.stop()

    # Verifica se os arquivos foram carregados
    if len(candidatos) == 0 or len(eleitores) == 0:
        print(Fore.RED + "\n❌ Você deve carregar candidatos e eleitores (Opções 1 e 2) antes de iniciar a votação.\n")
        time.sleep(3)
        input("\nPressione ENTER para retornar...")
        return

    # 1. Configuração da Urna (UF)
    uf_urna = input("Digite a UF da urna: ").strip().upper()
    if len(uf_urna) != 2:
        print(Fore.RED + "UF inválida! A UF deve ter 2 letras (ex: MG, SP).")
        input("\nPressione ENTER para retornar...")
        return
    
   
    def votar_cargo(cargo_sigla, eleitor_uf):
        cargo_info = CARGOS_INFO.get(cargo_sigla)
        cargo_nome = cargo_info['nome']
        digitos = cargo_info['digitos']
        
        print(Fore.CYAN + f"\n--- VOTO PARA {cargo_nome} ({digitos} DÍGITOS) ---")
        
        while True:
            voto = input(f"Informe o número para {cargo_nome} (ou B para branco): ").strip().upper()
            
            # Voto em Branco
            if voto == "B":
                print(Fore.YELLOW + "Voto em BRANCO.")
                tocar_som("silvio-santos-esta-certo-disso.mp3") # MÁH, vocÊ-está-Certo-Disso?
                confirm = input("Confirma voto em branco? (S/N): ").strip().upper()
                if confirm == "S":
                    tocar_som("confirma-urna.mp3") # a plin lin lin lin lin
                    time.sleep(1) # Pequena pausa para ouvir o som
                    return "B"
                continue

            # Voto Nulo (Não-numérico ou dígitos incorretos)
            if not voto.isdigit() or len(voto) != digitos:
                if not voto.isdigit():
                    print(Fore.YELLOW + "Entrada inválida.")
                else:
                    print(Fore.YELLOW + f"Número inválido ({len(voto)} dígitos). Esperado {digitos} dígitos.")
                
                print(Fore.YELLOW + "Voto será anulado.")
                tocar_som("silvio-santos-esta-certo-disso.mp3") # MÁH, vocÊ-está-Certo-Disso?
                confirm = input("Confirma voto nulo? (S/N): ").strip().upper()
                if confirm == "S":
                    tocar_som("confirma-urna.mp3") # a plin lin lin lin lin
                    time.sleep(1)
                    return "N"
                continue

            # Busca do candidato
            candidato_encontrado = None
            
            for c in candidatos:
                c_sigla = str(c.get("cargo")).strip().upper()
                c_numero = str(c.get("numero")).strip()
                c_uf = str(c.get("uf", "")).upper().strip()
                
                # Deve ser do cargo e número corretos
                if c_sigla == cargo_sigla and c_numero == voto:
                    # O candidato DEVE ser da UF do eleitor para ser válido.
                    if cargo_sigla != "P":
                        if c_uf == eleitor_uf:
                            candidato_encontrado = c
                            break 
                        continue 
                    else:
                        candidato_encontrado = c
                        break 
                         
            # Processa o resultado da busca
            if candidato_encontrado:
                print(Fore.GREEN + f"Candidato: {candidato_encontrado.get('nome')} | Partido: {candidato_encontrado.get('partido')}")
                
                # Silvio Santos vem aí
                tocar_som("silvio-santos-esta-certo-disso.mp3")

                confirm = input("Confirma (S/N)? ").strip().upper()
                if confirm == "S":
                    
                    tocar_som("confirma-urna.mp3")
                    time.sleep(0.8) # Pausa necessária para ouvir o "Pirililili" antes de limpar a tela
                    return voto 
                else:
                    continue
            else:
                # Candidato não encontrado (ou não é da UF do eleitor)
                print(Fore.YELLOW + "Candidato não encontrado! Voto Nulo.")
                
                # Lombardi
                tocar_som("silvio-santos-esta-certo-disso.mp3")

                confirm = input("Confirma voto nulo? (S/N): ").strip().upper()
                if confirm == "S":
                    tocar_som("confirma-urna.mp3")
                    time.sleep(1)
                    return "N"
                else:
                    continue
   

    # --- LOOP PRINCIPAL DE VOTAÇÃO 
    while True:
        limpar_tela()
        print(Fore.CYAN + "=" * 50)
        print(Fore.GREEN + Style.BRIGHT + f"   URNA ATIVA - VOTANDO EM: {uf_urna}")
        print(Fore.CYAN + "=" * 50)

        titulo_eleitor = input(Fore.YELLOW + "\nInforme o Título de Eleitor (ou 'SAIR' para encerrar a sessão): ").strip()
        
        if titulo_eleitor.upper() == "SAIR" or not titulo_eleitor:
            break 
            
        if titulo_eleitor in titulos_computados:
            print(Fore.RED + "🚫 O eleitor já votou.")
            input("\nENTER para continuar...")
            continue 
            
        # Busca do eleitor
        eleitor_encontrado = next((e for e in eleitores if str(e.get("titulo")).strip() == titulo_eleitor), None)

        if not eleitor_encontrado:
            print(Fore.RED + "🚫 Eleitor não encontrado ou Título inválido.")
            input("\nENTER para continuar...")
            continue
            
        eleitor_uf = eleitor_encontrado.get('uf').upper()
        if eleitor_uf != uf_urna:
            print(Fore.RED + f"🚫 Eleitor de {eleitor_uf} não pode votar nesta urna de {uf_urna}.")
            input("\nENTER para continuar...")
            continue

        print(Fore.GREEN + f"\nEleitor: {eleitor_encontrado.get('nome')}")
        print(Fore.GREEN + f"Estado: {eleitor_uf}")
        
        # Sequência de votação 
        cargos_sequencia = ["F", "E", "S", "G", "P"] 

        voto_eleitor = {"UF_URNA": uf_urna, "UF_ELEITOR": eleitor_uf, "TITULO": titulo_eleitor}
        
        # Coleta os 5 votos
        for sigla in cargos_sequencia:
            voto = votar_cargo(sigla, eleitor_uf) 
            voto_eleitor[sigla] = voto
        
        try:
            with open("votos.bin", "ab") as arquivo:
                pickle.dump(voto_eleitor, arquivo)
            titulos_computados.add(titulo_eleitor)
            print(Fore.GREEN + "\n✅ Voto registrado com sucesso e salvo em 'votos.bin'!")
        except Exception as e:
            print(Fore.RED + f"Erro ao salvar voto: {e}")

        continuar = input(Fore.YELLOW + "\nRegistrar novo voto (S ou N)? ").strip().upper()
        if continuar != 'S':
            break 

    print(Fore.MAGENTA + "\nSessão de votação encerrada.")
    input("Pressione ENTER para retornar ao menu principal...")
    return
        
            
# ==========================================================
# APURAÇÃO DOS VOTOS
# ==========================================================
def apurar_votos():
    limpar_tela()
    global resultados_apurados

    print(Fore.CYAN + "Iniciando apuração dos votos...")
    time.sleep(1)

    contagem = {}
    for sigla in CARGOS_INFO.keys():
        contagem[sigla] = {'validos': {}, 'brancos': 0, 'nulos': 0, 'total': 0}

    try:
        with open("votos.bin", "rb") as arquivo:
            while True:
                try:
                    voto = pickle.load(arquivo)
                    
                    for sigla in CARGOS_INFO.keys():
                        escolha = voto.get(sigla)
                        
                        contagem[sigla]['total'] += 1

                        if escolha == 'B':
                            contagem[sigla]['brancos'] += 1
                        elif escolha == 'N':
                            contagem[sigla]['nulos'] += 1
                        else:
                            if escolha in contagem[sigla]['validos']:
                                contagem[sigla]['validos'][escolha] += 1
                            else:
                                contagem[sigla]['validos'][escolha] = 1

                except EOFError:
                    break 
        
        resultados_apurados = contagem
        print(Fore.GREEN + "✔ Apuração concluída com sucesso!")
        print(Fore.YELLOW + "Vá para a opção 5 para ver os vencedores e gerar o boletim.")

    except FileNotFoundError:
        print(Fore.RED + "❌ Nenhum voto foi registrado ainda (arquivo 'votos.bin' não existe).")
    except Exception as e:
        print(Fore.RED + f"❌ Erro na apuração: {e}")

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
# CRIAR GRÁFICOS 
# ==========================================================

def gera_grafico(titulo, votos, brancos=0, nulos=0):
  

    # Junta candidatos + nulos
    nomes = list(votos.keys()) + ["Brancos","Nulos"]
    quantidades = list(votos.values()) + [brancos, nulos]

    # Gera cores diferentes para cada barra
    cores = []
    for _ in nomes:
        cores.append((random.random(), random.random(), random.random()))

    plt.figure(figsize=(12, 8))

    # GRÁFICO VERTICAL
    barras = plt.bar(nomes, quantidades, color=cores)

    plt.title(titulo, fontsize=18)
    plt.ylabel("Quantidade de votos", fontsize=14)
    plt.xlabel("Candidatos", fontsize=14)
    plt.xticks(rotation=45, ha='right')

    # Exibe valores acima das barras
    for barra in barras:
        height = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width()/2,  
            height + 0.3,                         
            str(int(height)),
            ha='center',
            va='bottom'
        )

    plt.tight_layout()
    plt.show()



# ==========================================================
# MOSTRAR RESULTADOS + BOLETIM
# ==========================================================
def mostrar_resultado():
    limpar_tela()
    
    if not resultados_apurados:
        print(Fore.RED + "❌ É necessário realizar a Apuração (Opção 4) antes de ver os resultados.")
        input("\nPressione ENTER para retornar...")
        return

    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + Style.BRIGHT + "RESULTADO DAS ELEIÇÕES")
    print(Fore.CYAN + "=" * 50 + "\n")

    conteudo_boletim = []
    conteudo_boletim.append("=" * 50)
    conteudo_boletim.append("BOLETIM DE URNA - UNILAVRAS 2025")
    conteudo_boletim.append("=" * 50 + "\n")

    ordem_exibicao = ["P", "G", "S", "F", "E"]

    for sigla in ordem_exibicao:
        info_cargo = CARGOS_INFO[sigla]
        dados_votos = resultados_apurados[sigla]
        
        titulo = f"--- {info_cargo['nome']} ---"
        print(Fore.YELLOW + titulo)
        conteudo_boletim.append(titulo)

        ranking = sorted(dados_votos['validos'].items(), key=lambda item: item[1], reverse=True)

        if len(ranking) == 0:
            msg = "Nenhum voto válido registrado para este cargo."
            print(msg)
            conteudo_boletim.append(msg)
        
        for numero_cand, qtd_votos in ranking:
            nome_candidato = "Desconhecido/Outra UF"
            partido_candidato = ""
            
            for c in candidatos:
                if c['numero'] == numero_cand and c['cargo'] == sigla:
                    nome_candidato = c['nome']
                    partido_candidato = c['partido']
                    break
            
            linha_result = f"{numero_cand} - {nome_candidato} ({partido_candidato}): {qtd_votos} votos"
            print(linha_result)
            conteudo_boletim.append(linha_result)
        
        votos_grafico = {}

        for c in candidatos:
            if c['cargo'] == sigla:
                chave = f"{c['nome']} ({c['numero']})"
                votos_grafico[chave] = dados_votos['validos'].get(c['numero'], 0)

        gera_grafico(
            f"Apuração - {info_cargo['nome']}",
            votos_grafico,
            nulos=dados_votos['nulos']
)        


        resumo = f"Brancos: {dados_votos['brancos']} | Nulos: {dados_votos['nulos']} | TOTAL: {dados_votos['total']}"
        print(Fore.CYAN + resumo + "\n")
        conteudo_boletim.append(resumo + "\n")
        conteudo_boletim.append("-" * 30)

    try:
        with open("boletim_urna.txt", "w", encoding="utf-8") as f:
            for linha in conteudo_boletim:
                f.write(linha + "\n")
        print(Fore.GREEN + "📄 Arquivo 'boletim_urna.txt' gerado com sucesso na pasta do projeto!")
    except Exception as e:
        print(Fore.RED + f"Erro ao gravar boletim: {e}")
        

    input("\nPressione ENTER para retornar...")
    return


# ==========================================================
# MENU PRINCIPAL
# ==========================================================
def menu():
    global candidatos_file, eleitores_file, candidatos, eleitores
    while True:
        limpar_tela() 
        print(f"{Fore.MAGENTA}\n" + "=" * 10 + "[ MENU PRINCIPAL ]" + "=" * 10)
        print("1 - Selecionar arquivo de Candidatos")
        print("2 - Selecionar arquivo de Eleitores")
        print("3 - Iniciar votação")
        print("4 - Apurar votos")
        print("5 - Mostrar resultados")
        print("6 - Fechar programa")
        print(Fore.MAGENTA +"=" * 38)
        print(Style.RESET_ALL)
        opcaoMenu = input("Digite a opção desejada: ").strip().upper()

        match opcaoMenu:
            case "BRASIL": # Se digitar BRASIL, o hino do maior do mundo vai tocar!!
                tocar_som("Hino do Brasil em 8-Bits.mp3") 
            case "1":
                ler_arquivo_candidatos()
            case "2":
                ler_arquivos_eleitores()
            case "3":
                iniciar_votacao()
            case "4":
                apurar_votos()
            case "5":
                mostrar_resultado()
            case "6":
                limpar_tela()
                print("\nEncerrando sistema...")
                time.sleep(1)
                print("✅ Sistema encerrado com sucesso!")
                break
            case _:
                print("Opção inválida!")



# ==========================================================
# INICIAR SISTEMA
# ==========================================================
if __name__ == "__main__":
    menu_boas_vindas()

    menu()
