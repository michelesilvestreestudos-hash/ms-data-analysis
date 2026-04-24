import pandas as pd
import os

# 1. Configuração de caminhos (Usando 'r' para evitar erros de barra no Windows)
caminho_input = r'michelesilvestreestudos-project\01-pipelines-python\202603_CPGF.csv'
caminho_output = r'michelesilvestreestudos-project\01-pipelines-python\resumo_gastos_marco.csv'

try:
    print("🚀 Iniciando processamento dos dados de Março/2026...")
    
    # 2. Carregamento com tratamento de encoding brasileiro
    df = pd.read_csv(caminho_input, sep=';', encoding='latin-1')

    # 3. Limpeza de Dados (Data Wrangling)
    # Garante que valores vazios virem zero e converte para número decimal
    df['VALOR TRANSAÇÃO'] = df['VALOR TRANSAÇÃO'].fillna('0')
    df['VALOR TRANSAÇÃO'] = (df['VALOR TRANSAÇÃO']
                             .str.replace('.', '', regex=False)
                             .str.replace(',', '.', regex=False)
                             .astype(float))

    # Converte a data (errors='coerce' evita que o código pare se houver data errada)
    df['DATA TRANSAÇÃO'] = pd.to_datetime(df['DATA TRANSAÇÃO'], format='%d/%m/%Y', errors='coerce')

    # --- ANÁLISES AUTOMÁTICAS ---

    # A. Top 10 Órgãos
    print("\n🏢 --- RANKING: ÓRGÃOS QUE MAIS GASTARAM ---")
    ranking_orgao = df.groupby('NOME ÓRGÃO')['VALOR TRANSAÇÃO'].sum().sort_values(ascending=False)
    print(ranking_orgao.head(10))

    # B. Perfil por Tipo (Busca automática da coluna correta)
    col_tipo = [c for c in df.columns if 'TIPO' in c or 'SUBGRUPO' in c]
    if col_tipo:
        nome_col = col_tipo[0]
        print(f"\n💳 --- DISTRIBUIÇÃO POR {nome_col} ---")
        perfil = df.groupby(nome_col)['VALOR TRANSAÇÃO'].agg(['count', 'sum']).sort_values(by='sum', ascending=False)
        perfil.columns = ['Qtd Transações', 'Total Gasto (R$)']
        print(perfil)

    # C. Maiores Notas Individuais
    print("\n💎 --- MAIORES COMPRAS INDIVIDUAIS (INSIGHTS DE GOVERNANÇA) ---")
    maiores_notas = df[['NOME FAVORECIDO', 'VALOR TRANSAÇÃO', 'NOME ÓRGÃO']].nlargest(10, 'VALOR TRANSAÇÃO')
    print(maiores_notas)

    # --- SEÇÃO DE CONSULTA PERSONALIZADA ---
    # Altere o termo abaixo para pesquisar o que quiser (Ex: 'Restaurante', 'Polícia', 'Hotel')
    termo_pesquisa = 'Polícia Federal' 
    print(f"\n🔍 --- BUSCA ESPECÍFICA POR: '{termo_pesquisa}' ---")
    
    # O filtro busca em 'NOME ÓRGÃO' ou 'NOME FAVORECIDO'
    resultado_busca = df[
        df['NOME ÓRGÃO'].str.contains(termo_pesquisa, na=False, case=False) |
        df['NOME FAVORECIDO'].str.contains(termo_pesquisa, na=False, case=False)
    ]
    
    print(resultado_busca[['DATA TRANSAÇÃO', 'NOME FAVORECIDO', 'VALOR TRANSAÇÃO']].head(15))

    # 4. Exportação dos resultados para CSV
    ranking_orgao.to_csv(caminho_output, sep=';', encoding='latin-1')
    print(f"\n✅ Sucesso! Resumo gerado em: {caminho_output}")

except FileNotFoundError:
    print(f"❌ ERRO: O arquivo '{caminho_input}' não foi encontrado.")
    print("Verifique se o nome do arquivo na pasta é exatamente esse.")
except PermissionError:
    print(f"❌ ERRO: Não pude salvar o arquivo de saída. Verifique se o Excel está com o arquivo '{caminho_output}' aberto.")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")

    # %%
    # D. Ranking de Instituições/Empresas (Onde o dinheiro foi gasto)
    print("\n🏢 --- TOP 10 INSTITUIÇÕES COM MAIOR RECEBIMENTO ---")
    
    # Agrupamos pelo nome da empresa/favorecido e somamos os valores
    ranking_estabelecimentos = (df.groupby('NOME FAVORECIDO')['VALOR TRANSAÇÃO']
                                .sum()
                                .sort_values(ascending=False))

    # Exibe os 10 primeiros
    print(ranking_estabelecimentos.head(10))

# %% [Célula 1: Importação e Carga]
import pandas as pd
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(diretorio_atual, '202603_CPGF.csv')

print(f"Tentando ler: {caminho}")

df = pd.read_csv(caminho, sep=';', encoding='latin-1')
df = pd.read_csv(caminho, sep=';', encoding='latin-1')

df['VALOR TRANSAÇÃO'] = df['VALOR TRANSAÇÃO'].fillna('0').str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
df['DATA TRANSAÇÃO'] = pd.to_datetime(df['DATA TRANSAÇÃO'], format='%d/%m/%Y', errors='coerce')

print("✅ Dados carregados e limpos com sucesso!")

# %% [Célula 3: Ranking de Instituições/Sellers]
print("\n🏪 --- TOP 10 INSTITUIÇÕES COM MAIOR RECEBIMENTO ---")

ranking_sellers = df.groupby('NOME FAVORECIDO')['VALOR TRANSAÇÃO'].sum().nlargest(10)

print(ranking_sellers)

top_1_nome = ranking_sellers.index[0]
print(f"\n🔍 Investigando o Top 1: {top_1_nome}")
detalhes_top = df[df['NOME FAVORECIDO'] == top_1_nome]
print(detalhes_top[['DATA TRANSAÇÃO', 'NOME ÓRGÃO', 'VALOR TRANSAÇÃO']].head(5))
