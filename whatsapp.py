import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

def processar_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
    
    dados = []
    padrao = r'^\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)$'
    
    mensagem_atual = ""
    for linha in linhas:
        match = re.match(padrao, linha)
        if match:
            if mensagem_atual:
                dados[-1][3] = mensagem_atual.strip()
            
            data, hora, remetente, mensagem = match.groups()
            dados.append([data, hora, remetente.strip(), mensagem])
            mensagem_atual = mensagem
        else:
            if dados:
                mensagem_atual += "\n" + linha
    
    df = pd.DataFrame(dados, columns=['data', 'hora', 'remetente', 'mensagem'])
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    return df

def mostrar_resumo(df):
    resumo = df['remetente'].value_counts()
    print("\nTotal de mensagens por remetente:")
    for remetente, total in resumo.items():
        print(f"{remetente}: {total} mensagens")
    return resumo

def mostrar_historico(df, remetente):
    historico = df[df['remetente'] == remetente]
    if historico.empty:
        print(f"\nNenhuma mensagem encontrada para {remetente}")
    else:
        print(f"\nHistórico de mensagens de {remetente}:")
        for _, row in historico.iterrows():
            print(f"[{row['data'].strftime('%d/%m/%Y')}, {row['hora']}] {row['mensagem']}")

def criar_grafico_historico_remetente(df, remetente):
    historico = df[df['remetente'] == remetente]
    
    if historico.empty:
        print(f"\nNenhuma mensagem encontrada para {remetente}")
        return
    
    mensagens_por_dia = historico['data'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    plt.hist(historico['data'], bins=min(30, len(mensagens_por_dia)), 
             edgecolor='black', alpha=0.7)
    
    plt.title(f'Histórico de mensagens de {remetente}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def criar_grafico_pizza(df):
    contagem = df['remetente'].value_counts()
    plt.figure(figsize=(10, 8))
    plt.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%')
    plt.title('Distribuição de mensagens por remetente')
    plt.axis('equal')
    plt.show()

def criar_grafico_linhas(df):
    mensagens_por_dia = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 6))
    for coluna in mensagens_por_dia.columns:
        plt.plot(mensagens_por_dia.index, mensagens_por_dia[coluna], 
                label=coluna, marker='o', markersize=4)
    
    plt.title('Mensagens por remetente ao longo do tempo')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():

            
    arquivo = input("\nCaminho do arquivo de chat: ")
                
    df = processar_arquivo(arquivo)
            
    while True:
        print("\nOpções:")
        print("1. Resumo das conversas")
        print("2. Histórico do remetente")
        print("3. Gráfico do histórico do remetente")
        print("4. Gráfico de pizza")
        print("5. Gráfico de linhas")
        print("6. Sair")
                
        opcao = input("\nEscolha uma opção (1-6): ")
                
        if opcao == '1':
            mostrar_resumo(df)
        elif opcao == '2':
            remetente = input("Digite o nome do remetente: ")
            mostrar_historico(df, remetente)
        elif opcao == '3':
            remetente = input("Digite o nome do remetente: ")
            criar_grafico_historico_remetente(df, remetente)
        elif opcao == '4':
            criar_grafico_pizza(df)
        elif opcao == '5':
            criar_grafico_linhas(df)
        elif opcao == '6':
            break
        else:
            print("Opção inválida!")
                    

if __name__ == "__main__":
    main()