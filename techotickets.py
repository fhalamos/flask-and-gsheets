from flask import Flask, redirect
from flask.json import jsonify
from flask import request

import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)


googleSheetDataBaseName = "Entradas Cine"

scope=""
creds=""
client=""
sheet=""

def initiateGoogleSheetsAccess():
	# use creds to create a client to interact with the Google Drive API
	global scope
	global creds
	global client

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)
	 
	


def checkIfTicketIsAvailable(ticketCode):
	global sheet
	sheet = client.open(googleSheetDataBaseName).sheet1

	#En la primera columna tenemos los codigos de los tickets
	codes_column = sheet.col_values(3)
	codes_column.pop(0)


	line_counter=2
	for code in codes_column:
		if code != "":
			if code == ticketCode:
				if sheet.cell(line_counter,4).value == "No":
					sheet.update_cell(line_counter,4,"Si")
	 				return "BIENVENIDO! ENTRADA CON CODIGO "+ ticketCode +" VALIDADA"
				else:
					return "ERROR! ENTRADA CON CODIGO "+ticketCode+ " YA FUE OCUPADA"
			line_counter = line_counter +1	

	return "NO SE ENCONTRO ENTRADA CON CODIGO "+ ticketCode




		

@app.route('/', methods=['GET'])
def checkTicket():

	return "hola"
	ticketCode = request.args.get('ticketCode')
	initiateGoogleSheetsAccess()
	return checkIfTicketIsAvailable(ticketCode)




if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
