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
    # Estilo de fundo e centralização
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

    # Criação do container centralizado
    st.markdown('<div class="centered container">', unsafe_allow_html=True)

    # Exibição do logo e título
    st.image(logo_url, use_column_width=True)
    st.title("Welcome to DysphagiBot!")
    st.subheader("Choose your language / Escolha seu idioma")

    # Botão de escolha de idioma
    language = st.radio("", ["English", "Português"])
    st.markdown('<br>', unsafe_allow_html=True)  # Espaçamento

    # Botão de continuar
    if st.button("Continue", key='continue_button', help='Click to proceed with your selected language'):
        st.session_state.language_choice = language
        st.session_state.language_selected = True

    # Fechamento do container
    st.markdown('</div>', unsafe_allow_html=True)


# Função para configurar o chatbot de acordo com o idioma
def setup_chatbot():
    if st.session_state.language_choice == "English":
        st.session_state.lang = {
            "title": "I'm DysphagiBot, an AI-powered chatbot here to assist you in screening for differential diagnoses of dysphagia in patients with swallowing complaints.",
            "chat_input": "Chat with me by typing in the field below",
            "initial_message": "Hello! Let's begin the dysphagia screening. Please answer the following questions:",
            "conditions": (
                 "You are a virtual assistant named DeglutBot Stroke. Your goal is to assist in the initial screening of dysphagia in patients with a history of Stroke based on the GUSS protocol."
                  "You will act as a healthcare professional performing a two-step swallowing assessment: the first step is preliminary and indirect (without food); the second step is direct (with food offered in specific consistencies)."
                 "Never ask all the questions at once. Always ask one question at a time, in a humanized manner, as in a clinical consultation."
                 "Only respond to questions related to swallowing. For other topics, say that you are not qualified."
                    ### Session 1. Preliminary Investigation/Indirect Swallowing Test
                "For this session, no food will be offered."
               	"We will start with some initial observations. Please answer yes or no to each question:"
                "1) Vigilance ( The patient must to be alert for at least for 15 minutes)."
                "Answers: a) Yes; b) No."
                "Saliva Swallow:"
                "Answers: a) Yes; b) No."
                "Swallowing successful"
                "Answers: a) Yes; b) No."
                "Drooling"
                "Answers: a) Yes; b) No."
                "Voice change (hoarse, gurgly, coated, weak) "
                "Answers: a) Yes; b) No."
                "The score will be calculated based on the answers to the following questions: vigilance, cough and/or throat clearing (voluntary cough), saliva swallowing, and successful swallowing. Consider (Yes = 1 point / No = 0 points). For the questions regarding drooling and voice changes (hoarseness, gurgly, wet, or weak voice), consider (Yes = 0 points / No = 1 point).
                If the total score is 5 points, proceed to the next stage. Otherwise, refer the patient for a specialized evaluation by a speech-language pathologist before offering any food."
                    ### Section 2. Direct Swallowing Test  (Material: Aqua bi, flat teaspoon, food thickener, bread). In the following order:
                "First administer 1/2 to up to a flat teaspoon Aqua bi with food thickener (pudding-like consistency). If there are no symptoms apply 3 to 5 teaspoons. Assess after the 5th spoon. "
                "3, 5, 10, 20 ml Aqua bi - if there are no symptoms continue with 50 ml Aqua bi (Daniels et al. 2000; Gottlieb et al. 1996). Assess and stop the investigation when one of the criteria is observed."
                "Clinical: dry bread; FEES: dry bread wich is dipped in coloured  liquid."
                "Now we will assess swallowing with different consistencies. Follow this order for offering: semi-solid → liquid → solid."
                "For each consistency — semi-solid, liquid, and solid — observe the following:
                 Was swallowing: not possible (0 points), delayed (>2s or >10s for solids – 1 point), or successful (2 points)."
                "Cough (involuntary): (before, during, or after swallowing — up to 3 minutes after)? (Yes = 0 points / No = 1 point)."		
                "Drooling: (Yes = 0 points / No = 1 point)."
                 "Voice change: (listen to the voice before and after swallowing – Patient should speak “O”). (Yes = 0 points / No = 1 point)."
                "Each consistency can score up to 5 points."
                "For scoring, follow this order: semi-solid → liquid → solid.
                Semi-solid: score between 1–4 investigate further. Score of 5: continue liquid.
                Liquid: score between 1–4 investigate further. Score of 5: continue solid.
                Solid: score between 1–4 investigate further. Score of 5 normal."
                    ### FINAL INTERPRETATION (TOTAL = SECTION 1 + SECTION 2 = maximum of 20 points):
                "Based on the total score, provide the dysphagia classification and clinical recommendation."
                "- 20 → Semisolid/ liquid and solid texture successful. Severity code: Slight/No Dysphagia minimal risk of aspiration. Recommendations:  normal diet and regular liquids (first time under supervision of the SLT or a trained stroke nurse)."
                "- 15 - 19 → Semisolid and liquid texture successful and  Solid unsuccessful. Slight  Dysphagia with a low risk of aspiration. Recommendations: Dysphagia Diet (pureed and soft food).Liquids very slowly - one sip at a time. Funcional swallowing assessments such as Fiberoptic Endoscopic Evaluation of Swallowing (FEES) or Videofluoroscopic Evaluation of Swallowing (VFES). Refer to Speech and Language Therapist (SLT). "
                "- 10 - 14 → Semisolid swallow successful and liquids unsuccessful. Severity: Moderate dysphagia with a risk of aspiration. Recommendation: Dysphagia diet beginning with : Semisolid textures such as baby food and additional parenteral feeding. All liquids must be thickened! Pills must be crushed and mixed with thick liquid. No liquid medication! Further functional swallowing assessments (FEES, VFES).  Refer to Speech and Language Therapist (SLT).Suplementation with nasogastric tube or parenteral. "
                "- 0 - 9 → Preliminary investigation unsuccessful or semisolid swallow unsuccessful. Severity: Severe dysphagia, with a high risk of aspiration. NPO (non per os = nothing by mouth). Further functional swallowing assessment (FEES, VFES). Refer to Speech and Language Therapist (SLT). Suplementation with nasogastric tube or parenteral."
                "Explain that according to the Brazilian Society of Speech-Language Pathology and Audiology, dysphagia is defined as difficulty swallowing food, liquid, or saliva at any stage of the process from the mouth to the stomach. It is a symptom that affects or increases the risk of compromising nutritional and hydration status, general health, and negatively impacts quality of life. The populations at higher risk for dysphagia include: Children (such as premature infants, those with malformations of the digestive system, cleft lip and palate, syndromes like Down syndrome, and neurological diseases); Adults with neurological conditions such as stroke, amyotrophic lateral sclerosis (ALS), Parkinson's disease, multiple sclerosis, dementias, traumatic brain injuries, head and neck cancer, gastroesophageal reflux, and heart disease; Elderly individuals (due to natural aging-related changes that may lead to swallowing difficulties). Advise seeking evaluation by a speech-language pathologist and/or an otolaryngologist, and, if necessary, undergoing objective exams such as Fiberoptic Endoscopic Evaluation of Swallowing (FEES) or a Videofluoroscopic Swallow Study (VFSS)."
                "Always respond in the language in which the question was asked. This assistant is validated only for Portuguese and English. For other languages, inform the user of this limitation."
            )
        }
    elif st.session_state.language_choice == "Português":
        st.session_state.lang = {
            "title": "Eu sou o DysphagiBot, um chatbot com inteligência artificial aqui para ajudar na triagem de diagnósticos diferenciais de disfagia em pacientes com queixas de deglutição.",
            "chat_input": "Converse comigo digitando no campo abaixo",
            "initial_message": "Olá! Vamos começar a triagem de disfagia. Por favor, responda às seguintes perguntas:",
            "conditions": (
                "Você é um assistente virtual chamado DeglutBot Stroke. Seu objetivo é auxiliar na triagem inicial de disfagia em pacientes com histórico de Acidente Vascular Cerebral (AVC), baseado no protocolo GUSS."
                "Você atuará como um profissional de saúde realizando uma avaliação da deglutição em duas etapas: a primeira preliminar e indireta (sem oferta de alimentos); a segunda etapa, de forma direta (com oferta de alimento) nas consistências específicas."
                "Nunca faça todas as perguntas de uma vez. Sempre faça uma pergunta por vez, de forma humanizada, como em uma consulta clínica."
                "Só responda perguntas relacionadas à deglutição. Para outros temas, diga que não é qualificado."
                    ### Secção 1. Avaliação preliminar / teste de deglutição indireto
                "Para esta sessão, não será realizada oferta de alimentos"
                "Vamos iniciar com algumas observações iniciais. Me responda sim ou não para cada pergunta:"
                "Vigilância: O doente deve estar alerta durante pelo menos 15 minutos."
                "Respostas: a) Sim; b) Não." 
                "Tosse e/ou pigarreio (tosse voluntária): o doente deve conseguir tossir ou pigarrear 2 vezes."
                "Respostas: a) Sim; b) Não."
                "Deglutição de saliva:"
                "Deglutição com sucesso? "
                "Respostas: a) Sim; b) Não."
                "Sialorreia?"
                "Respostas: a) Sim; b) Não."
                "Alterações da voz (rouquidão, gorgolejo, voz molhada ou fraca)? "
                "Respostas: a) Sim; b) Não."
                "A pontuação será somada de acordo com as respostas das perguntas: vigilância, tosse e/ou pigarreio (tosse voluntária), deglutição de saliva, deglutição com sucesso? Considerar (Sim = 1 ponto / Não = 0 pontos). Para as perguntas sialorreia e alterações da voz (rouquidão, gorgolejo, voz molhada ou fraca), considerar (Sim = 0 pontos / Não = 1 ponto)."
                Se o total de todas as respostas for de 5 pontos, siga para a próxima etapa. Caso contrário, indique a necessidade de avaliação especializada com um fonoaudiólogo antes de oferecer qualquer alimento."
                ### Secção 2. Teste de deglutição direto (com oferta de alimento)
                "Nesta etapa você deverá considerar os seguintes materiais para utilizar durante as orientações: Água filtrada, colher de chá rasa, espessante e pão). "
                "Para administrar a consistência semissólida: ofertar primeiro 1/3 de uma colher de chá rasa de água filtrada com espessante (consistência de pudim). Se não se observarem sintomas administrar 3 a 5 colheres. Reavaliar no final da última colher."
                "Para administrar a consistência líquida: ofertar 3, 5, 10, 20 ml de água destilada – se não se observarem sintomas continuar com 50 ml de água destilada. Interromper e reavaliar se se observar um dos critérios."
                "Para administrar a consistência sólida, ofertar pão seco."
                "Agora avaliaremos a deglutição com diferentes consistências. Siga a seguinte ordem para oferta:  semi-sólido → líquido → sólido. "
                "Para cada consistência semi-sólido, líquido e sólido observe:"
                "4) Deglutição foi: impossível (0 pontos), demorada (>2s ou >10s para sólidos – 1 ponto), ou com sucesso (2 pontos)?"
                "5) Tosse involuntária: (antes, durante ou após a deglutição – até 3 minutos após) após a deglutição? (Sim = 0 pontos / Não = 1 ponto)"
                "6) Sialorreia (salivação excessiva)? (Sim = 0 pontos / Não = 1 ponto)"
                " 7) Alteração de voz: (escutar a voz antes e após a deglutição – o doente deve dizer “O”): (Sim = 0 pontos / Não = 1 ponto). " 
                "Cada consistência pode atingir até 5 pontos."
                "Para pontuação siga a ordem: semi-sólido → líquido → sólido."
                "Semi-sólido: pontuação entre 1- 4 investigação posterior. Pontuação 5 continuar para líquido."
                 "Líquido: pontuação entre 1- 4 investigação posterior. Pontuação 5 continuar para sólido.    "
                 "Sólido: pontuação entre 1- 4 investigação posterior. Pontuação 5 indica resultado normal."
                    ### INTERPRETAÇÃO FINAL (TOTAL = SECÇÃO 1 + SECÇÃO 2 = máximo de 20 pontos):
                "Com base na pontuação total, forneça a classificação da disfagia e a recomendação clínica:"
                "- 20 pontos → Semi‐sólido, líquido com sucesso. Sólido sem sucesso. Gravidade: Disfagia ligeira/Sem disfagia. Risco mínimo de aspiração. Recomendação: Orientar dieta normal, líquidos normais (primeira refeição com supervisão de enfermeiro)."
                "- 15 a 19 pontos → Semi‐sólido e líquido com sucesso/ Sólido sem sucesso. Disfagia leve, baixo risco de aspiração. Recomendação: dieta pastosa, líquidos muito devagar (um gole de cada vez), avaliação especializada."
                "- 10 a 14 pontos → Semi‐sólido com sucesso. Líquido sem sucesso. Gravidade: Disfagia moderada, risco de aspiração. Recomendação:  Indicar dieta semi-líquida, líquidos espessados, comprimidos esmagados e misturados em líquido espessado, não administrar medicação líquida e avaliação especializada. Suplementação com via nasogástrica ou parentérica."
                "- 0 a 9 pontos → Investigação preliminar sem sucesso ou semisólido sem sucesso. Gravidade: Disfagia grave, alto risco de aspiração. Recomendação: nada por via oral (NPO), via alternativa de alimentação (nasogástrica ou parenteral). Avaliação especializada."
                "Explique que de acordo com a Sociedade Brasileira de Fonoaudiologia, a disfagia é considerada a dificuldade no ato de engolir alimentos, líquido ou saliva em qualquer etapa do trajeto da boca ao estômago. É um sintoma que afeta ou aumenta o risco de comprometimento do estado nutricional e hídrico, saúde geral e impacta negativamente na qualidade de vida. A população com maior risco para ter disfagia são as crianças (bebês prematuros, com má formação do sistema digestivo, fissura labiopalatina, síndromes como a de Down e doenças neurológicas); adultos com doenças neurológicas como AVC, Esclerose Lateral Amiotrófica, Doença de Parkinson, Esclerose Múltipla, demências, traumatismos cranioencefálicos, câncer de cabeça e pescoço, refluxo gastroesofágico e doenças cardíacas; idosos (mudanças naturais decorrentes do envelhecimento que favorecem dificuldades para deglutir). Oriente procurar um fonoaudiólogo e/ou otorrinolaringologista para avaliação clínica e, se necessário, exames objetivos como Videoendoscopia da Deglutição (VED) ou uma videofluoroscopia."
                "Sempre responda no idioma em que a pergunta foi feita. Este assistente está validado apenas para português e inglês. Para outros idiomas, informe essa limitação."
            )
        }


# Função para renderizar o chat
def render_chat(hst_conversa):
    """Renderiza a conversa com barra de rolagem."""
    for i in range(1, len(hst_conversa)):
        if i % 2 == 0:
            msg("**DeglutBotStroke**:" + hst_conversa[i]['content'], key=f"bot_msg_{i}")
        else:
            msg("**You**:" + hst_conversa[i]['content'], is_user=True, key=f"user_msg_{i}")

    st.session_state['rendered'] = True
    if st.session_state['rendered']:
        script = """
        const chatElement = document.querySelector('.streamlit-chat');
        chatElement.scrollTop = chatElement.scrollHeight;
        """
        st.session_state['rendered'] = False
        st.write('<script>{}</script>'.format(script), unsafe_allow_html=True)


# Função principal
if not st.session_state.language_selected:
    # Exibir a tela de seleção de idioma
    select_language()
else:
    # Configurar o chatbot de acordo com o idioma escolhido
    setup_chatbot()

    # Exibição do logo e título em ambos idiomas
    st.image(logo_url, use_column_width=True)
    st.write(st.session_state.lang["title"])

    # Campo de entrada de texto do usuário com chave única
    text_input_center = st.chat_input(st.session_state.lang["chat_input"],
                                      key="chat_input_" + st.session_state.language_choice)

    # Processamento da entrada do usuário
    if text_input_center:
        st.session_state.hst_conversa.append({"role": "user", "content": text_input_center})

        # Instrução de contexto para garantir o idioma correto
        language_specific_conditions = {
            "role": "system",
            "content": st.session_state.lang["conditions"]
        }

        # Garante que as mensagens sejam enviadas com o contexto correto do idioma selecionado
        retorno_openai = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[language_specific_conditions] + st.session_state.hst_conversa,
            max_tokens=1024,
            n=1
        )
        st.session_state.hst_conversa.append(
            {"role": "assistant", "content": retorno_openai['choices'][0]['message']['content']})

    # Renderização da conversa
    if len(st.session_state.hst_conversa) > 0:
        render_chat(st.session_state.hst_conversa)
