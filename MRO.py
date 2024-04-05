
import openai

chave_api = "CHAVE_OPENAI"
openai.api_key = chave_api

def gerar_problemas_consequencias(texto_inicial, n_variacoes=5):
    prompt = texto_inicial + "\n1. "
    resposta = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=prompt,
      temperature=0.7,
      max_tokens=150,
      n=5,
      stop="\n"
    )
    
    problemas_consequencias = []
    for i in range(n_variacoes):
        problema = resposta.choices[i].text.strip()
        problemas_consequencias.append(problema)
    
    return problemas_consequencias

def enviar_mensagem(mensagem, lista_mensagens=[], problemas_consequencias=[]):
    lista_mensagens.append(
        {"role": "user", "content": mensagem}
    )

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lista_mensagens,
    )

    if not problemas_consequencias:
        problemas_consequencias = gerar_problemas_consequencias("Pode resultar em:")
    
    resposta_bot = resposta["choices"][0]["message"]["content"]
    if "sugestões de problemas e consequências" in resposta_bot:
        for idx, pc in enumerate(problemas_consequencias, 1):
            resposta_bot += f"\n{idx}. {pc}"
    
    return resposta_bot, lista_mensagens, problemas_consequencias

lista_mensagens = []
problemas_consequencias = []
while True:
    texto = input("Eu: ")

    if texto.lower() == "sair":
        break
    else:
        resposta, lista_mensagens, problemas_consequencias = enviar_mensagem(texto, lista_mensagens, problemas_consequencias)
        print("Chatbot:", resposta)
