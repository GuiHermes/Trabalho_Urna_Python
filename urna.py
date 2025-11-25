from os import system, name
import pickle # Aula 19-11-2025 Ciclo 4
import time
from colorama import init, Fore, Style

init(autoreset=True)
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
titulos_computados = set() # guarda os titulos de eleitores que já votaram
resultados_apurados = {} # Variável pra armazenar a contagem dos votos
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
                confirm = input("Confirma voto em branco? (S/N): ").strip().upper()
                if confirm == "S":
                    return "B"
                continue

            # Voto Nulo (Não-numérico ou dígitos incorretos)
            if not voto.isdigit() or len(voto) != digitos:
                if not voto.isdigit():
                    print(Fore.YELLOW + "Entrada inválida.")
                else:
                    print(Fore.YELLOW + f"Número inválido ({len(voto)} dígitos). Esperado {digitos} dígitos.")
                    
                confirm = input("Confirma voto nulo? (S/N): ").strip().upper()
                if confirm == "S":
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
                        continue # Candidato é de outro estado, ignora e continua procurando.
                    
                   
                    else:
                        candidato_encontrado = c
                        break 
                         
            # Processa o resultado da busca
            if candidato_encontrado:
                print(Fore.GREEN + f"Candidato: {candidato_encontrado.get('nome')} | Partido: {candidato_encontrado.get('partido')}")
                confirm = input("Confirma (S/N)? ").strip().upper()
                if confirm == "S":
                    return voto # Retorna o número do candidato
                else:
                    continue
            else:
                # Candidato não encontrado (ou não é da UF do eleitor)
                print(Fore.YELLOW + "Candidato não encontrado! Voto Nulo.")
                confirm = input("Confirma voto nulo? (S/N): ").strip().upper()
                if confirm == "S":
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
            break # Sai do loop principal
            
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
            
        # Verifica se o eleitor pertence à UF da urna (Critério de zona)
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
        
        # Salvar voto
        try:
            with open("votos.bin", "ab") as arquivo:
                pickle.dump(voto_eleitor, arquivo)
            titulos_computados.add(titulo_eleitor)
            print(Fore.GREEN + "\n✅ Voto registrado com sucesso e salvo em 'votos.bin'!")
        except Exception as e:
            print(Fore.RED + f"Erro ao salvar voto: {e}")

        # Ponto de Controle de Continuação
        continuar = input(Fore.YELLOW + "\nRegistrar novo voto (S ou N)? ").strip().upper()
        if continuar != 'S':
            break # Sai do loop e retorna ao menu.

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

    # Estrutura para guardar a contagem
    # Exemplo: 'P': {'validos': {'13': 10, '22': 5}, 'brancos': 0, 'nulos': 0, 'total': 0}
    contagem = {}
    for sigla in CARGOS_INFO.keys():
        contagem[sigla] = {'validos': {}, 'brancos': 0, 'nulos': 0, 'total': 0}

    try:
        with open("votos.bin", "rb") as arquivo:
            while True:
                try:
                    # Lê um voto (dicionário) do arquivo binário
                    voto = pickle.load(arquivo)
                    
                    # Itera sobre os cargos (P, G, S, F, E)
                    for sigla in CARGOS_INFO.keys():
                        escolha = voto.get(sigla)
                        
                        contagem[sigla]['total'] += 1

                        if escolha == 'B':
                            contagem[sigla]['brancos'] += 1
                        elif escolha == 'N':
                            contagem[sigla]['nulos'] += 1
                        else:
                            # É um voto numérico (válido)
                            if escolha in contagem[sigla]['validos']:
                                contagem[sigla]['validos'][escolha] += 1
                            else:
                                contagem[sigla]['validos'][escolha] = 1

                except EOFError:
                    break # Fim do arquivo
        
        # Salva na variável global para ser usada em "Mostrar Resultados"
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
# MOSTRAR RESULTADOS + BOLETIM
# ==========================================================
def mostrar_resultado():
    limpar_tela()
    
    # Verifica se a apuração já foi feita
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

    # Ordem de exibição: Presidente, Governador, Senador, Deputados
    ordem_exibicao = ["P", "G", "S", "F", "E"]

    for sigla in ordem_exibicao:
        info_cargo = CARGOS_INFO[sigla]
        dados_votos = resultados_apurados[sigla]
        
        titulo = f"--- {info_cargo['nome']} ---"
        print(Fore.YELLOW + titulo)
        conteudo_boletim.append(titulo)

        # Ordenar os candidatos por número de votos (do maior para o menor)
        # item[0] é o numero do candidato, item[1] é a qtd de votos
        ranking = sorted(dados_votos['validos'].items(), key=lambda item: item[1], reverse=True)

        if len(ranking) == 0:
            msg = "Nenhum voto válido registrado para este cargo."
            print(msg)
            conteudo_boletim.append(msg)
        
        for numero_cand, qtd_votos in ranking:
            # Buscar nome do candidato na lista global 'candidatos'
            nome_candidato = "Desconhecido/Outra UF"
            partido_candidato = ""
            
            for c in candidatos:
                # Verifica se numero e cargo batem
                if c['numero'] == numero_cand and c['cargo'] == sigla:
                    nome_candidato = c['nome']
                    partido_candidato = c['partido']
                    break
            
            linha_result = f"{numero_cand} - {nome_candidato} ({partido_candidato}): {qtd_votos} votos"
            print(linha_result)
            conteudo_boletim.append(linha_result)

        # Resumo Brancos e Nulos
        resumo = f"Brancos: {dados_votos['brancos']} | Nulos: {dados_votos['nulos']} | TOTAL: {dados_votos['total']}"
        print(Fore.CYAN + resumo + "\n")
        conteudo_boletim.append(resumo + "\n")
        conteudo_boletim.append("-" * 30)

    # Gravar Boletim em TXT
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
        try:
            opcaoMenu = int(input("Digite a opção desejada: "))
            match opcaoMenu:
                case 1:
                    ler_arquivo_candidatos()
                case 2:
                    ler_arquivos_eleitores()
                case 3:
                    iniciar_votacao()
                case 4:
                    apurar_votos()
                case 5:
                    mostrar_resultado()
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
    menu_boas_vindas()
    menu()

