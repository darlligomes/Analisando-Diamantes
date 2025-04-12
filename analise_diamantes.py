import kagglehub as kh
import pandas as pd
from os import path, getcwd

caminho = kh.dataset_download("shivam2503/diamonds")
arquivo = path.join(caminho, 'diamonds.csv')
df = pd.read_csv(arquivo)

df.to_excel("diamonds.xlsx", index=False)

qtd_cortes = df['cut'].value_counts()
moda = df['price'].mode()[0]

print("\n Análise da Planilha de Diamantes 🔹")
print(f"\n Quantidade de Cortes:\n{qtd_cortes}")
print(f"\n Preço mais comum (moda): R$ {moda}")

print("\nEscolha o critério para ordenar os dados:" \
"\n1 - Preço" \
"\n2 - Cor" \
"\n3 - Claridade" \
"\n4 - Profundidade")

try:
    ordenacao = int(input("\nDigite o número da opção: "))
    if ordenacao not in [1, 2, 3, 4]:
        raise ValueError("Opção inválida.")
except ValueError as e:
    print(f"Erro: {e}")
    exit()

tipo_asc = input("Deseja ordenar do menor para o maior? (S/N): ").strip().upper()
Ascending = True if tipo_asc == 'S' else False

coluna_ordenacao = {
    1: 'price',
    2: 'color',
    3: 'clarity',
    4: 'depth'
}[ordenacao]

df = df.sort_values(coluna_ordenacao, ascending=Ascending)
traducao = {
    1: 'preço',
    2: 'cor', 
    3: 'claridade',
    4: 'profundidade'
}[ordenacao]

print(f"\n Top 10 Diamantes ordenados por {traducao}:\n")
print(df[['cut', 'color', 'clarity', 'price', 'depth']].head(10))

print(f"Buscar valor em específico por {traducao}? (S/N)")
resposta = input().strip().upper()

if resposta == 'S':
    valores = list(df[coluna_ordenacao].unique())
    print(f"disponíveis: ")
    for i, tipo in enumerate(valores, start=1):
        print(f'{i} - {tipo}')
        
    try:
        tipo_escolhido = int(input("Escolha o número do tipo:\n"))
    except:
        tipo_escolhido = int(input("Incorreto, escolha novamente o número do tipo:\n"))
    
    
    if tipo_escolhido < 1 or tipo_escolhido > len(valores):
        raise ValueError("Número fora do intervalo válido.")
    valor_escolhido = valores[tipo_escolhido - 1]
    
    if isinstance(valor_escolhido, str):
        filtro = f"{coluna_ordenacao} == '{valor_escolhido}'"
    else:
        filtro = f"{coluna_ordenacao} == {valor_escolhido}"
    
    if coluna_ordenacao != 'price':
        valor_medio = df.groupby(coluna_ordenacao)['price'].mean()
        valor_medio_especifico = valor_medio[valor_escolhido]

    
    resultado = df.query(filtro)
    print(f"\n Resultados filtrados por {coluna_ordenacao} = {valor_escolhido}:\n")
    print(resultado[['cut', 'color', 'clarity', 'price', 'depth']].head(10))
    print(f"Valor médio: R$ {valor_medio_especifico:.2f}")



nome_arquivo = f"diamonds_ordenado_por_{traducao}.xlsx"
caminho_salvo = path.join(getcwd(), nome_arquivo)
df.to_excel(caminho_salvo, index=False)
print(f"Planilha salva como {nome_arquivo} em {caminho_salvo}")
