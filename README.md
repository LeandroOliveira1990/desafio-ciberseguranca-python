# Desafio de Cibersegurança: Simulando Malware para Aprender Defesa 🛡️

Olá! Este é o meu repositório para o desafio **"Simulando um Malware de Captura de Dados Simples em Python e Aprendendo a se Proteger"**.

O objetivo deste projeto foi mergulhar no funcionamento de dois tipos comuns de malware (Ransomware e Keylogger) em um ambiente 100% controlado e educacional. A ideia não é criar ferramentas maliciosas, mas sim **entender como os atacantes pensam para que eu possa me tornar um defensor melhor**.

---

## ⚠️ AVISO ÉTICO E DE SEGURANÇA ⚠️

Todo o código neste repositório foi criado **EXCLUSIVAMENTE para fins educacionais**.

* **NÃO USE ESTES SCRIPTS** em qualquer máquina ou sistema sem autorização explícita do proprietário.
* **NÃO ME RESPONSABILIZO** pelo mau uso deste material. O uso indevido de ferramentas de cibersegurança é ilegal.
* **RECOMENDAÇÃO:** Execute estes scripts apenas em uma **Máquina Virtual (VM)** isolada, como VirtualBox ou VMware, para não afetar seu sistema principal.

---

## 🚀 Os Projetos

Eu implementei as duas simulações propostas no desafio.

### 1. Simulador de Ransomware (`ransomware_sim.py`)

Este script simula um ataque de ransomware, que criptografa os arquivos da vítima e exige um resgate.

#### O que ele faz?

1.  **Gera uma Chave:** Cria uma chave de criptografia simétrica (`chave.key`) usando a biblioteca `cryptography`.
2.  **Criptografa:** Varre o diretório em busca de arquivos de teste (no meu caso, limitei a `*.txt` para segurança) e usa a chave para criptografar o conteúdo deles.
3.  **Deixa a Nota:** Cria um arquivo `LEIA_PARA_RECUPERAR_SEUS_ARQUIVOS.txt` explicando (de forma simulada) o que aconteceu.
4.  **Descriptografa:** O script também tem a função de "salvador", que usa a mesma `chave.key` para reverter o processo e devolver os arquivos ao estado original.

#### 🛡️ Como eu aprendi a me defender disso:

* **BACKUPS! BACKUPS! BACKUPS!** Este é o ponto principal. Se eu tenho um backup recente e offline (ou em nuvem imutável), o ransomware perde todo o seu poder. A regra 3-2-1 (3 cópias, 2 mídias, 1 offline) nunca fez tanto sentido.
* **Não clique em tudo:** A maioria dos ransomwares entra por e-mails de phishing. Este projeto me fez ser 10x mais paranoico com anexos e links estranhos.
* **Mantenha tudo atualizado:** Manter o Windows, o navegador e outros softwares atualizados corrige as brechas que esses malwares usam para se espalhar.
* **Antivírus (EDR):** Soluções modernas não olham só a assinatura do arquivo, mas o *comportamento*. Um bom EDR veria um processo aleatório criptografando centenas de arquivos e o bloquearia na hora.

---

### 2. Simulador de Keylogger (`keylogger_sim.py`)

Este script simula um spyware que captura tudo o que é digitado e envia para o atacante.

#### O que ele faz?

1.  **Captura Teclas:** Usando a biblioteca `pynput`, ele "escuta" o teclado e registra cada tecla pressionada.
2.  **Salva em Log:** Armazena tudo em um arquivo de log local (`key_log.txt`).
3.  **Exfiltração de Dados:** Usando `threading`, ele inicia um temporizador. A cada 60 segundos (configurável), ele envia o conteúdo do arquivo de log por e-mail (usando `smtplib` e uma conta de teste do Gmail com "Senha de App") para o "atacante".
4.  **Limpeza:** Após enviar o e-mail, ele apaga o log local para não deixar rastros.

#### 🛡️ Como eu aprendi a me defender disso:

* **MFA (Autenticação de Múltiplos Fatores):** Esse é o matador de keyloggers! Mesmo que o atacante roube minha senha, ele não vai ter o código do meu celular ou a minha chave física (YubiKey). Isso torna a senha roubada quase inútil.
* **Gerenciadores de Senha:** Quando eu uso um gerenciador (como Bitwarden ou 1Password) para preencher senhas, eu não estou *digitando* a senha. O keylogger não captura nada!
* **Antivírus e Anti-Malware:** Um bom antivírus detecta esse tipo de comportamento (um programa escutando o teclado) e o bloqueia.
* **Firewall (Filtro de Saída):** Um firewall bem configurado perguntaria: "Por que esse programa estranho (`python.exe`) está tentando se conectar a um servidor de e-mail (`smtp.gmail.com`)?". Isso poderia bloquear o *envio* dos dados.

---

## 💡 Meus Principais Aprendizados com este Desafio

Este projeto foi um grande "abrir de olhos" para mim.

1.  **O Poder das Ferramentas Simples:** Fiquei surpreso como, com poucas linhas de Python e bibliotecas conhecidas, é possível criar a base de algo tão perigoso. Isso mostra que a barreira de entrada para criar malware é mais baixa do que eu imaginava.
2.  **Segurança em Camadas:** Não existe uma "bala de prata". A defesa eficaz é uma soma de várias coisas: backups (contra ransomware) + MFA (contra keyloggers) + antivírus (pega os dois) + conscientização (previne a infecção inicial).
3.  **MFA não é opcional:** Antes deste projeto, eu via o MFA como algo "legal de se ter". Agora eu vejo como **essencial**. Vou ativar em todas as contas que puder.
4.  **O Fator Humano é Real:** No fim das contas, tanto o ransomware (phishing) quanto o keylogger (abrir um anexo infectado) dependem de uma falha humana. Treinamento e conscientização são, talvez, a defesa mais importante de todas.

Obrigado pelo desafio!
