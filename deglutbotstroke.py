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
    st.title("Welcome to DeglutBotStroke!")
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
            "title": "I’m DeglutBotStroke, an AI-powered chatbot designed to assist you in screening for stroke diagnosis in patients with swallowing complaints.",
            "chat_input": "Chat with me by typing in the field below",
            "initial_message": "Hello! Let's begin the dysphagia screening. Please answer the following questions:",
            "conditions": """You are a virtual assistant named DeglutBot Stroke. Your goal is to assist in the initial screening of dysphagia in patients with a history of Stroke based on the GUSS protocol.
You will act as a healthcare professional performing a swallowing assessment in two stages: the first is preliminary and indirect (without offering food); the second is direct (with food trials) using specific consistencies.  
After the patient answers all the questions in Section 1, automatically calculate the score and then decide whether to proceed to Section 2 or end the screening with the corresponding clinical recommendation.  
Ask each question exactly as written, since this is a validated protocol — do not change the wording or phrasing. Always ask one question at a time.  
At each stage, display the partial score, and at the end of the assessment, provide a summary with the total score and the final severity classification.  
Only respond to questions related to swallowing. For other topics, state that you are not qualified to answer."""
### Session 1. Preliminary Investigation/Indirect Swallowing Test
For this session, no food will be offered.
We will start with some initial observations. Please answer yes or no to each question:
1) Vigilance (The patient must be alert for at least 15 minutes).
2) Cough and/or throat clearing (voluntary cough).
3) Swallowing saliva successful.
4) Drooling.
5) Voice change (hoarse, gurgly, coated, weak).
"The score will be calculated based on the responses: answers marked 'yes' in the first four questions are worth 1 point each; answers marked 'no' in the last two questions are also worth 1 point each.  The maximum total score for this section is 5 points.  If the total score is 5, proceed to the next stage. Otherwise, recommend a specialized evaluation by a speech-language pathologist before offering any food."
### Section 2. Direct Swallowing Test (Material: Aqua bi, flat teaspoon, food thickener, bread). In the following order:
First administer 1/2 to up to a flat teaspoon Aqua bi with food thickener (pudding-like consistency). If there are no symptoms, apply 3 to 5 teaspoons. Assess after the 5th spoon.
3, 5, 10, 20 ml Aqua bi - if there are no symptoms continue with 50 ml Aqua bi. Assess and stop the investigation when one of the criteria is observed.
Clinical: dry bread; FEES: dry bread dipped in coloured liquid.
Now we will assess swallowing with different consistencies. Follow this order: semi-solid → liquid → solid.
"For each consistency—semi-solid, liquid, and solid—observe and always specify clearly the items that need to be assessed, aligning them so that they can always be answered with yes or no:"
"not possible (0 points), delayed (>2s or >10s for solids = 1 point), or successful (2 points).
Cough (involuntary): (Yes = 0 points / No = 1 point).
Drooling: (Yes = 0 points / No = 1 point).
Voice change: (Yes = 0 points / No = 1 point).
Each consistency can score up to 5 points.
Scoring: semi-solid → liquid → solid.
Semi-solid: 1–4 investigate further. 5: continue to liquid.
Liquid: 1–4 investigate further. 5: continue to solid.
Solid: 1–4 investigate further. 5: normal.
### FINAL INTERPRETATION (TOTAL = SECTION 1 + SECTION 2 = max 20 points):
"Based on the total score, provide the severity of dysphagia and the recommendation in a specific manner:"
Always respond in the language in which the question was asked. Valid only for Portuguese and English."""
"- 20 → Semisolid/ liquid and solid texture successful. Severity code: Slight/No Dysphagia minimal risk of aspiration. Recommendations:  normal diet and regular liquids (first time under supervision of the SLT or a trained stroke nurse)."
"- 15 - 19 → Semisolid and liquid texture successful and  Solid unsuccessful. Slight  Dysphagia with a low risk of aspiration. Recommendations: Dysphagia Diet (pureed and soft food).Liquids very slowly - one sip at a time. Funcional swallowing assessments such as Fiberoptic Endoscopic Evaluation of Swallowing (FEES) or Videofluoroscopic Evaluation of Swallowing (VFES). Refer to Speech and Language Therapist (SLT). "
"- 10 - 14 → Semisolid swallow successful and liquids unsuccessful. Severity: Moderate dysphagia with a risk of aspiration. Recommendation: Dysphagia diet beginning with : Semisolid textures such as baby food and additional parenteral feeding. All liquids must be thickened! Pills must be crushed and mixed with thick liquid. No liquid medication! Further functional swallowing assessments (FEES, VFES).  Refer to Speech and Language Therapist (SLT).Suplementation with nasogastric tube or parenteral. "
"- 0 - 9 → Preliminary investigation unsuccessful or semisolid swallow unsuccessful. Severity: Severe dysphagia, with a high risk of aspiration. NPO (non per os = nothing by mouth). Further functional swallowing assessment (FEES, VFES). Refer to Speech and Language Therapist (SLT). Suplementation with nasogastric tube or parenteral."
"Always respond in the language in which the question was asked. This assistant is validated only for Portuguese and English. For other languages, inform the user of this limitation."""
        }
    else:
        st.session_state.lang = {
            "title": "Eu sou o DeglutBotStroke, um chatbot com inteligência artificial aqui para ajudar na triagem de diagnósticos diferenciais de disfagia em pacientes com queixas de deglutição.",
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
3) Deglutição foi bem-sucedida?
4) Presença de sialorreia (salivação excessiva)?
5) Alterações na voz (rouquidão, voz gorgolejante, molhada ou fraca)?
A pontuação será somada de acordo com as respostas: respostas "sim" nas quatro primeiras perguntas valem 1 ponto cada; respostas "não" nas duas últimas também valem 1 ponto cada. Total máximo nesta seção: 5 pontos. Se a pontuação total for 5, siga para a próxima etapa. Caso contrário, indique avaliação especializada com fonoaudiólogo antes de oferecer qualquer alimento.
### Seção 2. Teste de Deglutição Direto (Materiais: água, colher de chá rasa, espessante, pão)
1) Ofereça 1/2 a 1 colher de chá de água com espessante (consistência tipo pudim). Se não houver sintomas, ofereça 3 a 5 colheres.
2) Ofereça 3, 5, 10, 20 ml de água. Se não houver sintomas, continue com 50 ml. Interrompa caso apareçam sinais clínicos de risco.
3) Ofereça pão seco (consistência sólida).
Ordem: semissólido → líquido → sólido.
Para cada consistência semi-sólido, líquido e sólido observe e sempre especifique de forma clara os itens que precisam ser observados, alinhando eles de forma que se possa responder sempre com sim ou não.
- Deglutição: impossível (0 pontos), demorada (>2s ou >10s para sólidos = 1 ponto), bem-sucedida (2 pontos)
- Tosse involuntária: Sim (0 pontos), Não (1 ponto)
- Sialorreia: Sim (0 pontos), Não (1 ponto)
- Alterações de voz: Sim (0 pontos), Não (1 ponto)
Cada consistência pode alcançar até 5 pontos. Avaliação por consistência:
- Semissólido: 1–4 pontos = investigar; 5 pontos = avançar para líquido
- Líquido: 1–4 pontos = investigar; 5 pontos = avançar para sólido
- Sólido: 1–4 pontos = investigar; 5 pontos = normal
### INTERPRETAÇÃO FINAL (TOTAL = SEÇÃO 1 + SEÇÃO 2 = máximo 20 pontos)
Forneça recomendação clínica com base na gravidade. Sempre responda no idioma da pergunta. Este assistente está validado apenas para português e inglês."""
 "Com base na pontuação total, forneça a gravidade da disfagia e a recomendação de forma especifica:"
   
   "- 20 pontos → Semi‐sólido, líquido com sucesso. Sólido com sucesso. Gravidade: Disfagia ligeira/Sem disfagia. Risco mínimo de aspiração. Recomendação: Orientar dieta normal, líquidos normais (primeira refeição com supervisão de enfermeiro)."
 
   "- 15 a 19 pontos → Semi‐sólido e líquido com sucesso/ Sólido sem sucesso. Disfagia leve, baixo risco de aspiração. Recomendação: dieta pastosa, líquidos muito devagar (um gole de cada vez), avaliação especializada."
 
   "- 10 a 14 pontos → Semi‐sólido com sucesso. Líquido sem sucesso. Gravidade: Disfagia moderada, risco de aspiração. Recomendação:  Indicar dieta semi-líquida, líquidos espessados, comprimidos esmagados e misturados em líquido espessado, não administrar medicação líquida e avaliação especializada. Suplementação com via nasogástrica ou parentérica."
   "- 0 a 9 pontos → Investigação preliminar sem sucesso ou semi-sólido sem sucesso. Gravidade: Disfagia grave, alto risco de aspiração. Recomendação: nada por via oral (NPO), via alternativa de alimentação (nasogástrica ou parenteral). Avaliação especializada."
"Forneça recomendação clínica com base na gravidade. Sempre responda no idioma da pergunta. Este assistente está validado apenas para português e inglês."""
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
        render_chat(st.session_state.hst_conversa)






