# Gspread é uma Python API para lidar com o Google Sheets.
import gspread 
from gspread import Worksheet 

# Importação para lidar com as informações de credenciais.
from oauth2client.service_account import ServiceAccountCredentials

# Define as credenciais de acesso à API do Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 
         'https://www.googleapis.com/auth/drive']

# Define as credenciais de acesso à API do Google Sheets.
creds = ServiceAccountCredentials.from_json_keyfile_name('diretório_da_keyfile.json', scope)
print(creds)
client = gspread.authorize(creds)

# Abre a planilha pelo ID do Google Sheets
sheet = client.open_by_key('código_da_pasta').worksheet('nome_da_página') # Substitua pelo ID da sua planilha e pela sua aba

# Busca a coluna de CPF e cria um dicionário para armazenar o índice de cada CPF
cpf_col = sheet.col_values(4, value_render_option='FORMULA') # Índice da coluna CPF
cpf_dict = {}
for i, cpf in enumerate(cpf_col[1:], start=2):
    cpf = str(cpf).zfill(11)  # Converte o valor para string e adiciona zeros à esquerda, se necessário
    if cpf in cpf_dict:
        cpf_dict[cpf].append(i)
    else:
        cpf_dict[cpf] = [i]

# Atualiza CPFs com menos de 11 dígitos na planilha
for cpf, indices in cpf_dict.items():
    if len(cpf) < 11:
        for index in indices:
            sheet.update_cell(index, 4, cpf) # Atualiza o CPF na planilha

# Remove a última linha duplicada para cada CPF e imprime a linha apagada
rows_to_remove = []
for cpf, indices in cpf_dict.items():
    if len(indices) > 1:
        for index_to_remove in sorted(indices[1:], reverse=True): # Começa do último índice e segue em ordem reversa
            rows_to_remove.append(index_to_remove)

# Remove as linhas duplicadas e imprime as linhas removidas
rows_to_remove = sorted(rows_to_remove, reverse=True)
for row in rows_to_remove:
    print(sheet.row_values(row)) # Imprime a linha antes de removê-la
    sheet.delete_rows(row)
