import os
import uuid
from dotenv import load_dotenv
import json
import requests
import streamlit as st
from langchain_core.messages import HumanMessage

from agents.agent import Agent

load_dotenv('../config/.keys')


def populate_envs(sender_email, receiver_email, subject):
    os.environ['FROM_EMAIL'] = sender_email
    os.environ['TO_EMAIL'] = receiver_email
    os.environ['EMAIL_SUBJECT'] = subject


def send_email(sender_email, receiver_email, subject, thread_id):
    try:
        populate_envs(sender_email, receiver_email, subject)
        config = {'configurable': {'thread_id': thread_id}}
        st.session_state.agent.graph.invoke(None, config=config)
        st.success('Epost sendt!')
        # Clear session state
        for key in ['travel_info', 'thread_id']:
            st.session_state.pop(key, None)
    except Exception as e:
        st.error(f'Feilet ved sending av epost: {e}')


def initialize_agent():
    if 'agent' not in st.session_state:
        st.session_state.agent = Agent()


def render_custom_css():
    st.markdown(
        '''
        <style>
        .main-title {
            font-size: 2.5em;
            color: #333;
            text-align: center;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        .main-title-small {
            font-size: 1.8em;
            color: #333;
            text-align: center;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        .sub-title {
            font-size: 1.2em;
            color: #333;
            text-align: left;
            margin-bottom: 0.5em;
        }
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .query-box {
            width: 80%;
            max-width: 600px;
            margin-top: 0.5em;
            margin-bottom: 1em;
        }
        .query-container {
            width: 80%;
            max-width: 600px;
            margin: 0 auto;
        }
        </style>
        ''', unsafe_allow_html=True)


def render_ui():
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">✈️ 🏨️ </div>',unsafe_allow_html=True)
    st.markdown('<div class="main-title-small">Agentbasert Verktøy for Søk og Turforslag til Eventyrlige Destinasjoner (AVSTED)</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="query-container">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Oppgi reiseønsker og få forslag på fly og hotell:</div>',
                unsafe_allow_html=True)
    user_input = st.text_area(
        'Reiseforespørsel',
        height=200,
        key='query',
        placeholder='Skriv reiseønskene dine her...',
    )
    st.markdown('</div>', unsafe_allow_html=True)
    # st.sidebar.image('kaboom.png', caption='AVSTED (AI Virtual Service for Travel and Event Design)',
    #                  use_column_width=True)

    return user_input


def process_query(user_input):
    if user_input:
        try:
            thread_id = str(uuid.uuid4())
            st.session_state.thread_id = thread_id

            messages = [HumanMessage(content=user_input)]
            config = {'configurable': {'thread_id': thread_id}}

            result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)

            st.subheader('Reiseforslag')
            st.write(result['messages'][-1].content)

            st.session_state.travel_info = result['messages'][-1].content

        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.error('Vennligst oppgi reiseønskene dine.')


def render_email_form():
    send_email_option = st.radio('Ønsker du informasjonen tilsendt på e-post?', ('Nei', 'Ja'))
    if send_email_option == 'Ja':
        with st.form(key='email_form'):
            sender_email = st.text_input('Avsender epost')
            receiver_email = st.text_input('Mottaker epost')
            subject = st.text_input('Emne', 'Reiseforslag')
            submit_button = st.form_submit_button(label='Send epost')

        if submit_button:
            if sender_email and receiver_email and subject:
                send_email(sender_email, receiver_email, subject, st.session_state.thread_id)
            else:
                st.error('Vennligst fyll ut alle feltene.')


def main():
    initialize_agent()
    render_custom_css()
    user_input = render_ui()

    if st.button('Lag reiseforslag'):
        process_query(user_input)

    if 'travel_info' in st.session_state:
        render_email_form()


if __name__ == '__main__':
    main()
