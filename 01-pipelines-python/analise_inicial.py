import pandas as pd

# Simulação de um pequeno dicionário de dados
dados = {
    'Nome': ['Michele', 'João', 'Ana', None],
    'Cargo': ['Data Scientist', 'Developer', 'Designer', 'Tester'],
    'Status': ['Ativo', 'Ativo', 'Inativo', 'Ativo']
}

# Criando um DataFrame
df = pd.DataFrame(dados)

print("--- Dados Brutos ---")
print(df)

# Uma pequena limpeza: removendo linhas com valores nulos
df_limpo = df.dropna()

print("\n--- Dados após Limpeza (Remoção de Nulos) ---")
print(df_limpo)

print("\nPrimeiro teste de push concluído com sucesso!")