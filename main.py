from flask import Flask, render_template, request, jsonify, session
from process_pdf import extrair_texto_pdf
from chatbot import gerar_feedback, gerar_resposta
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = "um_segredo_aleatorio_para_sessoes"  # necessário para usar session

# Lista de PDFs disponíveis
arquivos_pdf = ["requisitos.pdf", "requisitos2.pdf", "requisitos3.pdf"]

def carregar_contexto():
    # Se já tem um PDF escolhido na sessão, mantém o mesmo
    if "caminho_pdf" not in session:
        session["caminho_pdf"] = random.choice(arquivos_pdf)
        session["contexto"] = extrair_texto_pdf(session["caminho_pdf"])
    return session["contexto"]

@app.route('/')
def index():
    # Garante que a sessão tem um contexto carregado
    carregar_contexto()
    return render_template('index.html')

@app.route('/pergunta', methods=['POST'])
def pergunta():
    contexto = carregar_contexto()
    pergunta = request.form['pergunta']

    if pergunta.lower().strip() == "sair":
        # aqui podemos guardar a conversa inteira em session, se quiser
        conversa = session.get("historico", [])
        resposta = gerar_feedback(conversa)
    else:
        resposta = gerar_resposta(pergunta, contexto)
        # opcional: armazenar histórico
        historico = session.get("historico", [])
        historico.append(f"Aluno: {pergunta}\nStakeholder: {resposta}")
        session["historico"] = historico

    data_hora = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return jsonify({'resposta': resposta, 'data_hora': data_hora})


if __name__ == "__main__":
    app.run(debug=True)