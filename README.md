# 🗳 Urna Eletrônica Simplificada

**Simulação didática do processo eleitoral brasileiro usando Python**

Este projeto implementa uma **urna eletrônica simplificada**, totalmente
escrita em Python, com fins **educacionais**.\
Ela permite carregar candidatos e eleitores, registrar votos,
armazená-los em arquivo binário e realizar toda a apuração.

------------------------------------------------------------------------

## 🚀 Começando

Estas instruções ajudam a rodar o projeto localmente para
**desenvolvimento, estudos e testes**.

------------------------------------------------------------------------

## 📋 Pré-requisitos

-   Python **3.8+**
-   Terminal: CMD, PowerShell, Bash, etc.

Verifique sua versão:

``` bash
python --version
```

------------------------------------------------------------------------

## 🔧 Instalação

### 1️⃣ Clone o repositório

``` bash
git clone https://github.com/GuiHermes/Trabalho_Urna_Python
```

### 2️⃣ Entre no projeto

``` bash
cd urna-eletronica
```

### 3️⃣ Execute o programa

``` bash
python src/urna.py
```

### 4️⃣ Prepare os arquivos necessários

Coloque em `/dados`:

-   `candidatos.txt`
-   `eleitores.txt`

Exemplo (`candidatos.txt`):

    João Silva,12,ABC,SP,P
    Maria Souza,45,XYZ,SP,F

Exemplo (`eleitores.txt`):

    12345678900
    98765432100
    11122233344

------------------------------------------------------------------------

## 📚 Funcionalidades

-   Carregar candidatos
-   Carregar eleitores
-   Votação com verificação
-   Registro binário dos votos (`pickle`)
-   Apuração de votos válidos, brancos e nulos
-   Boletim de urna

------------------------------------------------------------------------

## 🔩 Testes de ponta a ponta (E2E)

1.  Carregar candidatos\
2.  Carregar eleitores\
3.  Votar\
4.  Gerar `votos.pkl`\
5.  Apurar resultados\
6.  Exibir boletim de urna

------------------------------------------------------------------------

## ✨ Estrutura de Pastas

    urna-eletronica/
    │
    ├── dados/
    │   ├── candidatos.txt
    │   ├── eleitores.txt
    │   └── votos.pkl
    │
    ├── src/
    │   ├── urna.py
    │   ├── funcoes_votacao.py
    │   ├── funcoes_arquivos.py
    │   └── funcoes_apuracao.py
    │
    └── README.md

------------------------------------------------------------------------

## 🧪 Testes de estilo (opcional)

``` bash
pip install black flake8 pylint
black src/
flake8 src/
pylint src/
```

------------------------------------------------------------------------

## 📦 Implantação

Execute:

``` bash
python src/urna.py
```

Opcional no Windows --- criar `iniciar.bat`:

    python src/urna.py
    pause

------------------------------------------------------------------------

## 🛠 Tecnologias

-   Python 3\
-   Pickle\
-   OS / time\
-   CLI (terminal)

------------------------------------------------------------------------

## ✒ Autores

-   Guilherme Hermes --- https://github.com/GuiHermes\
-   Manuel Victor --- https://github.com/mvmce\
-   Hian Oliveira --- https://github.com/hian128\
-   Matheus Rodrigues --- https://github.com/Matheus-Rod03

------------------------------------------------------------------------
