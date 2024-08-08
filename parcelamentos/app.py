import os
from flask import Flask, request, jsonify
import pymssql
from decimal import Decimal
from datetime import datetime

app = Flask(__name__)

# Dados de conexão
server = 'prd-db-juridico.database.windows.net'
database = 'bigdataJuridico'
username = 'usrjuridico'
password = 'XNDe4W6SlnM5dz43ZW7r'

def format_value(value):
    if isinstance(value, Decimal):
        return f"{value:,.2f}"
    elif isinstance(value, datetime):
        return value.strftime("%m/%Y")
    return value

def busca_par(cnpj):
    try:
        connection = pymssql.connect(server=server, user=username, password=password, database=database)
        print("Conexão estabelecida com sucesso.")
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM LeadParcelados WHERE CpfCnpjDoOptante = '{cnpj}'")

        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = {columns[i]: format_value(value) for i, value in enumerate(row)}
            results.append(row_dict)

        cursor.close()
        connection.close()
        print("Conexão encerrada com sucesso.")

        return results

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/parcelamentos', methods=['GET'])
def get_parcelamentos():
    cnpj = request.args.get('cnpj')
    if not cnpj:
        return jsonify({'error': 'CNPJ não fornecido'}), 400
    
    resultados = busca_par(cnpj)
    if resultados is None:
        return jsonify({'error': 'Erro ao buscar dados'}), 500

    return jsonify(resultados), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
