import os
import sys
from io import StringIO
from PIL import Image
from dotenv import load_dotenv
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
import streamlit as st

os.environ["REQUESTS_CA_BUNDLE"] = "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"
load_dotenv('../config/.keys')

config_list_bedrock = [
    {
        "api_type": "bedrock",
        "model": "anthropic.claude-3-sonnet-20240229-v1:0",
        "aws_region": os.getenv("AWS_REGION"),
        "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "price": [0.003, 0.015],
        "temperature": 0.1,
        "cache_seed": None,
    }
]


if __name__ == '__main__':
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    work_dir = "generated_code"
    st.title("Autokoder!")
    task = st.text_area("**Oppdrag**", key="user_input", height=200)
    web = st.checkbox("Netttilgang", key="netttilgang")

    col1, col2 = st.columns(2)
    with col1:
        run = st.button("Start utvikling")
    with col2:
        clear_all = st.button("Nullstill", on_click=lambda: st.session_state.clear())

    web_append = """ Legg til import os og set os.environ["REQUESTS_CA_BUNDLE"] = '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem'"""

    task_desc = task + web_append if web else task

    if run:
        developer = autogen.AssistantAgent(
            "Utvikler",
            llm_config={
                "config_list": config_list_bedrock,
            },
        )

        team_lead = autogen.UserProxyAgent(
            "Teamleder",
            human_input_mode="NEVER",
            code_execution_config={
                "executor": LocalCommandLineCodeExecutor(work_dir=work_dir),
            },
            is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
            max_consecutive_auto_reply=10,
        )

        team_lead.initiate_chat(
            developer,
            message=task_desc,
            summary_method="reflection_with_llm",
        )

    # Reset stdout
    sys.stdout = old_stdout

    # Display console output in Streamlit
    st.markdown("### Konsoll")
    st.text(mystdout.getvalue())

    image_path = f"{work_dir}/meta_vs_tsla.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption='Meta vs Tesla hittil i år', use_column_width=True)
