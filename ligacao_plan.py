import gspread
from google.oauth2 import service_account
import pandas as pd

def buscar_itens(worksheet_name):
    #Configuração inicial
    service_account_info = ["GOOGLE_SERVICE_ACCOUNT"]
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file('file.json', scopes=scope)

    #Nome da planilha
    name_sheet = 'Cálculo Faturamento - Teste Robô'
    # Depois atualizar para buscar pelo id
    #1y9nv8ctqf1z0z4wx8G15GX18Qxb5IQ-w-1gdCLp1zBU

    # Nome da aba
    #worksheet_name = 'Relação de CH - Faturamento'

    sa = gspread.authorize(credentials)
    sh = sa.open(name_sheet)
    list1 = sh.sheet1.get()
    wks = sh.worksheet(worksheet_name)
    itens = pd.DataFrame(list1)
    
    itens.info()


    # Restante é pandas
    
    # Tratar nome de colunas

    # A linha com os cabeçalhos é a segunda (índice 1)
    
    itens.columns = itens.iloc[1] # Usamos o `.iloc[1]` para pegar essa linha e transformar-la nas novas colunas

    
    itens = itens.drop(index=1) # Remover a segunda linha, que agora já foi usada como cabeçalho
    itens = itens.drop(index=0)

    # Definir as colunas
    # Filtrar apenas status diferente de "Ok"
    itens = itens[(itens['Codigo_Status'] != '1') & (itens['Codigo_Status'] != '3')]

    # verificar se irá rodar com os itens que mostraram erro

    return itens,wks

def busca_worksheet(worksheet_name):
    #Configuração inicial
    service_account_info = ["GOOGLE_SERVICE_ACCOUNT"]
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file('file.json', scopes=scope)

    #Nome da planilha
    name_sheet = 'Cálculo Faturamento - Teste Robô'
    # Depois atualizar para buscar pelo id
    #1y9nv8ctqf1z0z4wx8G15GX18Qxb5IQ-w-1gdCLp1zBU

    # Nome da aba
    # worksheet_name = 'IMPOSTOS'

    sa = gspread.authorize(credentials)
    sh = sa.open(name_sheet)
    wks = sh.worksheet(worksheet_name)
    list1 = wks.get_all_values()
    
    itens = pd.DataFrame(list1)
    itens.columns = itens.iloc[0]
    itens = itens.drop(index=0)

    filtro_status = itens['STATUS'] != "Sucesso"
    itens = itens[filtro_status]

    return itens,wks


# itens, sheet = busca_worksheet("IMPOSTOS")
# for index, row in itens.iterrows():
#         intervalo = f'A{index+2}:H{index+2}'
#         teste = "testando1"
#         teste2 = "teste2"
#         sheet.update(intervalo,[[teste,teste2]])
#         intervalo