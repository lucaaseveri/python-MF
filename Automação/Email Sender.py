import os
import sys
import smtplib
import imghdr
import time
import pandas as pd
from random import randrange
from email.message import EmailMessage

'''
Projeto por Lucas Severi.

Necessidade: Empresa quer mandar boletos para os clientes via email.
> Sujeito: Boleto Condomínio
> Texto com nome personalizado e com "Segue em anexo o boleto"
> Boleto específico da casa em anexo

Recursos:
> Pasta com boletos em pdf ordenados de acordo com os contatos no BD
> BD em excel
> Coluna de email nomeada: email
> Coluna de nome nomeada: nome

Restrição:
> Não conter email/senha no código, armezanados em variáveis do ambiente
> Ter backlog de quais emails foram enviados
'''

# Nome da coluna do email
nome_coluna_email = 'email'
# Nome da coluna do nome
nome_coluna_nome = 'nome' 


# 1. with smtplib.SMTP('localhost', 1025) as smtp:
# 1. SERVER ON CMD
# 1. RUN ON CMD = python -m smtpd -c DebuggingServer -n localhost:1025
	
# Vari
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Caminho dos pdfs
CAMINHO_SEP = '/Users/Adm/Desktop/Python Scripts/Separados/'
NOME_EXCL = 'Cadastro.xlsx'

# Pega a coluna do excel
df = pd.read_excel(NOME_EXCL, sheet_name=0)
mail_list = df[nome_coluna_email].tolist()
first_name_list = df[nome_coluna_nome].tolist()

# Transformando nome inteiro em primeiro nome
name_list = ['None']*len(first_name_list)
for i in range(len(first_name_list)):
	name_list[i] = (first_name_list[i].split(" ")[0]).capitalize()


# Lista para contatos sem email
vazio_list = []

# backlog caso dê error
history_file = open('history.txt', 'w') 
counter = 0
email_vazio = 0

# Pega o numero de files na pasta
list = os.listdir(CAMINHO_SEP)
number_files = len(list)

# Verificar possível error
if(number_files != len(mail_list)):
	print("Numero de PDF's e Emails não condizem")
	
else:
	for i in range(number_files):
		# Se a linha nao for vazia
		if(not pd.isna(mail_list[i])):
			msg = EmailMessage()
			msg['Subject'] = 'Boleto Condomínio'
			msg['From'] = EMAIL_ADDRESS
			msg['To'] = mail_list[i]
			msg.set_content("Olá %s! Segue em anexo o boleto." % (name_list[i]))
			
			files = [CAMINHO_SEP+'pdf-%i.pdf' %(i+1)]
			
			for file in files:
				with open(file, 'rb') as f:
					file_data = f.read()
					# file_name = 'pagina_%i.pdf' %(i+i)
					file_name = 'Boleto.pdf'
					
					msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
				
			with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
				smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
				smtp.send_message(msg)
				print("Email para %s enviado!" %(mail_list[i]))
				history_file.write("Email para %s enviado!\n" %(mail_list[i]))
				counter=counter+1
		elif(pd.isna(mail_list[i])):
			email_vazio = email_vazio+1
			print("Morador %s sem email cadastrado :(" %(first_name_list[i]))
			vazio_list.append(first_name_list[i])
	time.sleep(2 + randrange(9))
	
	history_file.write("%i emails enviados!\n" %(counter))
	history_file.write("%i contatos cadastrados!\n\n\n" %(counter+email_vazio))
	for k in range(len(vazio_list)):
		history_file.write("Contatos sem emails cadastrados:\n")
		history_file.write("%s\n" %(vazio_list[k]))
	if(counter == number_files):
		print("Feito!")
	elif (email_vazio>0):
		print("Algum morador nao tem email cadastrado")
	else:
		print("Confira se algo deu errado!")
history_file.close()
print("\n\n---Aperte enter para fechar---")
input()
sys.exit(0)