🗳 Urna Eletrônica Simplificada

Uma urna eletrônica desenvolvida em Python para fins didáticos.
Este projeto simula o processo eleitoral brasileiro de forma simplificada, permitindo carregar arquivos de candidatos e eleitores, registrar votos, armazená-los em arquivo binário e realizar a apuração final.

🚀 Começando

Estas instruções permitirão que você obtenha uma cópia do projeto funcionando na sua máquina para desenvolvimento e testes.
Na seção Implantação, você encontrará instruções para executar o sistema em um ambiente final.

📋 Pré-requisitos

Antes de começar, você precisará instalar:

Python 3.8+

Sistema operacional com suporte a terminal (Windows, Linux ou macOS)

Instalando o Python

Baixe e instale o Python em:

https://www.python.org/downloads/


Após instalar:

python --version


Deve retornar algo como:

Python 3.10.2

🔧 Instalação

Siga os passos abaixo para configurar o ambiente:

1. Faça o clone do repositório
git clone https://github.com/seu-usuario/urna-eletronica

2. Entre na pasta do projeto
cd urna-eletronica

3. Execute o programa principal
python src/urna.py

4. Prepare os arquivos necessários

Dentro da pasta /dados coloque:

candidatos.txt

eleitores.txt

Exemplo de candidatos:

João Silva,12,ABC,SP,P
Maria Souza,45,XYZ,SP,F


Repita a estrutura conforme os requisitos do projeto.

Após a configuração, basta rodar novamente o programa e navegar pelo menu.

⚙ Executando os testes

Atualmente o projeto não utiliza testes automatizados formais, mas você pode testar:

Consistência dos arquivos

Funcionalidade da votação

Apuração dos votos

Tratamento de votos nulos e em branco

Recomendação: criar arquivos pequenos para testes.

🔩 Testes de ponta a ponta

Este tipo de teste garante que todo o fluxo funcione corretamente:

Carregar candidatos

Carregar eleitores

Votar

Registrar votos no arquivo binário

Apurar votos

Gerar boletim de urna

Eles validam o sistema como um todo, testando o uso real.

Exemplo:

Cadastrar 3 eleitores e 3 candidatos

Realizar 3 votações

Verificar se o arquivo votos.pkl foi criado corretamente

Apurar e conferir os totais

⌨ Testes de estilo de código

O projeto pode opcionalmente usar ferramentas como:

flake8

pylint

black

Eles garantem boa formatação, limpeza e padronização do código.

Exemplo de uso:

pip install black
black src/

📦 Implantação

Para implantar o projeto em uma máquina final, recomenda-se:

Criar um ambiente virtual (opcional)

Definir caminhos fixos para os arquivos de candidatos/eleitores

Executar o programa via terminal ou criar um atalho para o arquivo principal

Bloquear alterações externas nos arquivos de dados durante a votação

Exemplo de execução:

python src/urna.py

🛠 Construído com

Ferramentas e tecnologias utilizadas:

Python 3 — Linguagem de programação

Pickle — Serialização de votos em arquivo binário

OS / time — Controles de sistema e espera

Terminal interativo — Interface baseada em console

✒ Autores

A equipe responsável por desenvolver o projeto:

Guilherme Hermes 
GitHub: https://github.com/GuiHermes

Manuel Victor  
GitHub: https://github.com/mvmce

Hian Oliveira 
GitHub: https://github.com/hian128

Matheus Rodrigues 
GitHub: https://github.com/Matheus-Rod03

Você também pode ver todos os colaboradores que participaram deste projeto na aba Contributors do repositório.