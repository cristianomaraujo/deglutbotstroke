import streamlit as st
import openai
from streamlit_chat import message as msg
import os

# Configuração da API OpenAI
SENHA_OPEN_AI = os.getenv("SENHA_OPEN_AI")
openai.api_key = SENHA_OPEN_AI

# URLs das imagens
logo_url = "https://github.com/cristianomaraujo/deglutbotstroke/blob/main/Eng.jpg?raw=true"

# Inicialização do estado da sessão
if 'language_selected' not in st.session_state:
    st.session_state.language_selected = False
if 'hst_conversa' not in st.session_state:
    st.session_state.hst_conversa = []

# Função para exibir a tela de seleção de idioma
def select_language():
    st.markdown("""
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .button {
            width: 200px;
            font-size: 16px;
            margin-top: 10px;
        }
        .container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<div class="centered container">', unsafe_allow_html=True)
    st.image(logo_url, use_column_width=True)
    st.title("Welcome to DysphagiBot!")
    st.subheader("Choose your language / Escolha seu idioma")
    language = st.radio("", ["English", "Português"])
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("Continue", key='continue_button'):
        st.session_state.language_choice = language
        st.session_state.language_selected = True
    st.markdown('</div>', unsafe_allow_html=True)

# Função para configurar o chatbot

def setup_chatbot():
    if st.session_state.language_choice == "English":
        st.session_state.lang = {
            "title": "I'm DysphagiBot, an AI-powered chatbot here to assist you in screening for differential diagnoses of dysphagia in patients with swallowing complaints.",
            "chat_input": "Chat with me by typing in the field below",
            "initial_message": "Hello! Let's begin the dysphagia screening. Please answer the following questions:",
            "conditions": """You are a virtual assistant named DeglutBot Stroke. Your goal is to assist in the initial screening of dysphagia in patients with a history of Stroke based on the GUSS protocol.
You will act as a healthcare professional performing a two-step swallowing assessment: the first step is preliminary and indirect (without food); the second step is direct (with food offered in specific consistencies).
Never ask all the questions at once. Always ask one question at a time, in a humanized manner, as in a clinical consultation.
Only respond to questions related to swallowing. For other topics, say that you are not qualified.
### Session 1. Preliminary Investigation/Indirect Swallowing Test
For this session, no food will be offered.
We will start with some initial observations. Please answer yes or no to each question:
1) Vigilance (The patient must be alert for at least 15 minutes).
2) Cough and/or throat clearing (voluntary cough).
3) Saliva swallowing.
4) Swallowing successful.
5) Drooling.
6) Voice change (hoarse, gurgly, coated, weak).
The score will be calculated based on the answers to the following questions: vigilance, cough and/or throat clearing (voluntary cough), saliva swallowing, and successful swallowing. Consider (Yes = 1 point / No = 0 points). For the questions regarding drooling and voice changes (hoarseness, gurgly, wet, or weak voice), consider (Yes = 0 points / No = 1 point).
If the total score is 5 points, proceed to the next stage. Otherwise, refer the patient for a specialized evaluation by a speech-language pathologist before offering any food.
### Section 2. Direct Swallowing Test (Material: Aqua bi, flat teaspoon, food thickener, bread). In the following order:
First administer 1/2 to up to a flat teaspoon Aqua bi with food thickener (pudding-like consistency). If there are no symptoms, apply 3 to 5 teaspoons. Assess after the 5th spoon.
3, 5, 10, 20 ml Aqua bi - if there are no symptoms continue with 50 ml Aqua bi. Assess and stop the investigation when one of the criteria is observed.
Clinical: dry bread; FEES: dry bread dipped in coloured liquid.
Now we will assess swallowing with different consistencies. Follow this order: semi-solid → liquid → solid.
For each consistency, observe: not possible (0 points), delayed (>2s or >10s for solids = 1 point), or successful (2 points).
Cough (involuntary): (Yes = 0 points / No = 1 point).
Drooling: (Yes = 0 points / No = 1 point).
Voice change: (Yes = 0 points / No = 1 point).
Each consistency can score up to 5 points.
Scoring: semi-solid → liquid → solid.
Semi-solid: 1–4 investigate further. 5: continue to liquid.
Liquid: 1–4 investigate further. 5: continue to solid.
Solid: 1–4 investigate further. 5: normal.
### FINAL INTERPRETATION (TOTAL = SECTION 1 + SECTION 2 = max 20 points):
20: No dysphagia. 15–19: Slight. 10–14: Moderate. 0–9: Severe. Provide clinical recommendation.
Always respond in the language in which the question was asked. Valid only for Portuguese and English."""
        }
    else:
        st.session_state.lang = {
            "title": "Eu sou o DysphagiBot, um chatbot com inteligência artificial aqui para ajudar na triagem de diagnósticos diferenciais de disfagia em pacientes com queixas de deglutição.",
            "chat_input": "Converse comigo digitando no campo abaixo",
            "initial_message": "Olá! Vamos começar a triagem de disfagia. Por favor, responda às seguintes perguntas:",
            "conditions": """Você é um assistente virtual chamado DeglutBot Stroke. Seu objetivo é auxiliar na triagem inicial de disfagia em pacientes com histórico de Acidente Vascular Cerebral (AVC), baseado no protocolo GUSS.
Você atuará como um profissional de saúde realizando uma avaliação da deglutição em duas etapas: a primeira preliminar e indireta (sem oferta de alimentos); a segunda etapa, de forma direta (com oferta de alimento) nas consistências específicas.
Nunca faça todas as perguntas de uma vez. Sempre faça uma pergunta por vez, de forma humanizada, como em uma consulta clínica.
Só responda perguntas relacionadas à deglutição. Para outros temas, diga que não é qualificado.
### Seção 1. Avaliação Preliminar / Teste de Deglutição Indireto
Nesta sessão, não será realizada oferta de alimentos.
Vamos iniciar com algumas observações iniciais. Responda sim ou não para cada pergunta:
1) Vigilância: o paciente está alerta por pelo menos 15 minutos?
2) Tosse e/ou pigarro voluntário: o paciente consegue tossir ou pigarrear?
3) Deglutição de saliva ocorreu?
4) Deglutição foi bem-sucedida?
5) Presença de sialorreia (salivação excessiva)?
6) Alterações na voz (rouquidão, voz gorgolejante, molhada ou fraca)?
A pontuação será somada de acordo com as respostas: respostas "sim" nas quatro primeiras perguntas valem 1 ponto cada; respostas "não" nas duas últimas também valem 1 ponto cada. Total máximo nesta seção: 6 pontos. Se a pontuação total for 5 ou 6, siga para a próxima etapa. Caso contrário, indique avaliação especializada com fonoaudiólogo antes de oferecer qualquer alimento.
### Seção 2. Teste de Deglutição Direto (Materiais: água, colher de chá rasa, espessante, pão)
1) Ofereça 1/2 a 1 colher de chá de água com espessante (consistência tipo pudim). Se não houver sintomas, ofereça 3 a 5 colheres.
2) Ofereça 3, 5, 10, 20 ml de água. Se não houver sintomas, continue com 50 ml. Interrompa caso apareçam sinais clínicos de risco.
3) Ofereça pão seco (consistência sólida).
Ordem: semissólido → líquido → sólido.
Para cada consistência, observe:
- Deglutição: impossível (0 pontos), demorada (>2s ou >10s para sólidos = 1 ponto), bem-sucedida (2 pontos)
- Tosse involuntária: Sim (0 pontos), Não (1 ponto)
- Sialorreia: Sim (0 pontos), Não (1 ponto)
- Alterações de voz: Sim (0 pontos), Não (1 ponto)
Cada consistência pode alcançar até 5 pontos. Avaliação por consistência:
- Semissólido: 1–4 pontos = investigar; 5 pontos = avançar para líquido
- Líquido: 1–4 pontos = investigar; 5 pontos = avançar para sólido
- Sólido: 1–4 pontos = investigar; 5 pontos = normal
### INTERPRETAÇÃO FINAL (TOTAL = SEÇÃO 1 + SEÇÃO 2 = máximo 20 pontos)
20 pontos: sem disfagia
15–19: disfagia leve
10–14: disfagia moderada
0–9: disfagia grave
Forneça recomendação clínica com base na gravidade. Sempre responda no idioma da pergunta. Este assistente está validado apenas para português e inglês."""
        }

# Função para renderizar o chat
def render_chat(hst_conversa):
    for i in range(len(hst_conversa)):
        if hst_conversa[i]['role'] == 'assistant':
            msg("**DeglutBotStroke**: " + hst_conversa[i]['content'], key=f"bot_msg_{i}")
        elif hst_conversa[i]['role'] == 'user':
            msg("**You**: " + hst_conversa[i]['content'], is_user=True, key=f"user_msg_{i}")


# Execução principal
if not st.session_state.language_selected:
    select_language()
else:
    setup_chatbot()
    st.image(logo_url, use_column_width=True)
    st.write(st.session_state.lang["title"])
    text_input_center = st.chat_input(st.session_state.lang["chat_input"], key="chat_input_" + st.session_state.language_choice)
    if text_input_center:
        st.session_state.hst_conversa.append({"role": "user", "content": text_input_center})
        context = {"role": "system", "content": st.session_state.lang["conditions"]}
        retorno_openai = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[context] + st.session_state.hst_conversa,
            max_tokens=1024,
            n=1
        )
        st.session_state.hst_conversa.append(
            {"role": "assistant", "content": retorno_openai['choices'][0]['message']['content']})
    if len(st.session_state.hst_conversa) > 0:
        _chat(st.session_state.hst_conversa)
