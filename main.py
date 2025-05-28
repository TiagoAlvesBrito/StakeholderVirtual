from flask import Flask, render_template, request, jsonify
from process_pdf import extrair_texto_pdf
from chatbot import gerar_resposta
from datetime import datetime

app = Flask(__name__)
caminho_pdf = "requisitos.pdf"
contexto = extrair_texto_pdf(caminho_pdf)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pergunta', methods=['POST'])
def pergunta():
    pergunta = request.form['pergunta']
    resposta = gerar_resposta(pergunta, contexto)
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'resposta': resposta, 'data_hora': data_hora})

if __name__ == "__main__":
    app.run(debug=True)