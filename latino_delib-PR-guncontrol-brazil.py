import streamlit as st
import os
from utils.session import session_setup
from streamlit_theme import st_theme
from utils.components import (show_response_count, finish_button, done_button, show_finish_status,
                              add_reaction_buttons, get_input_and_gen_response, comments)
def setup():
    os.environ['country'] = 'Brasil'
    os.environ['topic'] = 'o controle de armas'

    os.environ['intro_temp'] = '0.7'
    os.environ['intro_top_p'] = '0.9'
    os.environ['intro_rep_pen'] = '1'
    os.environ['intro_max_tokens'] = '512'

    os.environ['intro_system_instruction'] = "Responda com uma lista de prós e contras sobre o tema em questão."
    os.environ['intro_text'] = f"""Imagine que você é uma pessoa do {os.environ['country']} moderando uma discussão sobre {os.environ['topic']}]. Com base nos valores culturais do {os.environ['country']}, forneça ao seu companheiro de comunicação argumentos sobre por que uma pessoa média do {os.environ['country']} estaria a favor ou contra {os.environ['topic']}. Você deve fornecer informações em um estilo casual em português. Comece a conversa exatamente com o seguinte aviso:

    \"Boa tarde. Serei seu companheiro de conversa hoje em uma breve discussão sobre {os.environ['topic']}. Esta discussão é uma oportunidade para você aprender sobre {os.environ['topic']}. Quero encorajá-lo a falar livremente. Não se espera que você seja um especialista. Além disso, não é necessário chegar a um consenso, você não precisa concordar com as posturas que eu fornecer. Meu papel é te ajudar a aprender como as pessoas no Brasil percebem os prós e os contras de {os.environ['topic']}.\"

    E então forneça informações culturalmente relevantes em uma lista de prós e contras.

    Por último, incentive a conversa terminando com \"Por favor, comece nos contando algo que te confunde sobre este tema.\"
    """

    os.environ['gen_temp'] = '0.7'
    os.environ['gen_top_p'] = '0.9'
    os.environ['gen_rep_pen'] = '1'
    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = f"Termine a sua resposta dentro de {os.environ['gen_max_tokens']} tokens."


def chat_bubble_css():
    if st.session_state['current_theme'] == "dark":
        background_color_user = "#027148"
        background_color_bot = "#434343"
    else:
        background_color_user = "#dcf8c6"
        background_color_bot = "#f1f0f0"

    st.markdown(f"""
        <style>
        .chat-container {{
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }}
        .user-message, .bot-message {{
            padding: 10px;
            border-radius: 15px;
            max-width: 60%;
            margin: 5px;
            position: relative;
            margin-top: 15px;  /* Staggered positioning for each message */
        }}
        .user-message {{
            align-self: flex-end;
            background-color: {background_color_user};
        }}
        .bot-message {{
            align-self: flex-start;
            background-color: {background_color_bot};
        }}
        </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    layout='wide',
    page_title='AI chatbot',
    page_icon='🤖'
)


def main():
    setup()
    session_setup()
    chat_bubble_css()

    if st.session_state.get('next_page', False):
        st.session_state.current_page = "feedback"  # Set the current page in session state

    current_page = st.session_state.get('current_page', "chat")

    if current_page == "feedback":
        show_feedback_page()
    else:
        show_chat_page()


def show_chat_page():
    st.title('AI chatbot')
    introduction = st.session_state['introduction']
    st.info(introduction)

    # Display chat history
    for i, exchange in enumerate(st.session_state.get('chat_history', [])):
        user_message = exchange['user_input']
        bot_response = exchange['response']

        st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">{user_message}</div>
                <div class="bot-message">{bot_response}</div>
            </div>
        """, unsafe_allow_html=True)

        add_reaction_buttons(i)

    get_input_and_gen_response()
    show_response_count()
    finish_button()
    show_finish_status()


def show_feedback_page():
    st.subheader("Chatbot Responses for Feedback")
    st.write("""
    On this page, you can provide feedback on the chatbot's responses.
    
    Below, you will see a list of input / response pairs from your chat. Your input is in ***green***, while the 
    chatbot's response is in ***gray***.
    
    To the right of a response, you can click **Yes** under **Give feedback?** if you want to provide feedback on that 
    response, or you can click **No** if not. 
    
    If you choose to provide feedback on a response, you can specify the type by choosing from the categories in the 
    dropdown menu. You can choose more than one. Then, fill out the comment box with your thoughts on the response.
    
    You must provide feedback for at least two responses, at which point a **Submit** button will appear at the bottom
    of the page.
    
    Click **Submit** when you are finished, then click **Go to post-survey** to take the post-survey.
    """)

    with st.expander("Click to learn what each category means"):
        st.markdown("""
        - **Balanced / biased towards certain perspective**: ...
        - **Morally + ethically sound / morally + ethically questionable**: ...
        - **Factually incorrect**: ...
        - **Respectful / disrespectful**: ...
        - **Culturally relevant / culturally irrelevant**: ...
        - **Other**: Any other feedback that doesn't fit into the above categories.
        <br><br>
        """, unsafe_allow_html=True)

    comments()
    #done_button()

    if 'done_pressed' in st.session_state and st.session_state['done_pressed']:
        st.success("Comments submitted! Click **Go to post-survey** to start the post-survey.")


if __name__ == '__main__':
    main()
