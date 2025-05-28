import openai

import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(pergunta, contexto):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um stakeholder virtual, proprietário de uma empresa que precisa de um software. "
                    "Seu papel é responder a perguntas de estudantes que estão praticando técnicas de entrevista "
                    "para elicitação de requisitos, ajudando-os a identificar requisitos funcionais e não funcionais. "
                    "Responda como um cliente real: inclua ambiguidades, informações incompletas e evite listar requisitos diretamente. "
                    "Dê respostas curtas, para incentivar o estudante a perguntar mais. Não termine as respostas com perguntas. "
                    "Se o estudante escrever 'sair', forneça um feedback estruturado sobre os pontos fortes e fracos da entrevista."
                ),
            },
            {"role": "user", "content": f"Contexto: {contexto}"},
            {"role": "user", "content": pergunta},
        ],
        temperature=0.3,  # Controla a criatividade - para manter respostas realistas, sem muita aleatoriedade
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # Teste simples
    contexto = "O sistema deve permitir compras online de ingressos."
    pergunta = "Quais são os principais atores do sistema?"
    resposta = gerar_resposta(pergunta, contexto)
    print("Resposta do chatbot:", resposta)
