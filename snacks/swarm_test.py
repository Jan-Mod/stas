from swarm import Swarm, Agent
from dotenv import load_dotenv
import os
# import httpx
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"
load_dotenv('../config/.keys')


# Dette må endres i Swarm() klassen for at det skal funke på sb1u nett. Man må overstyre http_klienten fordi OpenAI
# ikke godtar selvsignerte sertifikater. api_key må også settes manuelt når det gjøres slik
# class Swarm:
#     def __init__(self, client=None, api_key=None, http_client=None):
#         if not client:
#             client = OpenAI(api_key=api_key, http_client=http_client)
#         self.client = client
# httpx_client = httpx.Client(verify=False)
#client = Swarm(api_key=os.getenv("OPENAI_API_KEY"), http_client=httpx_client)

client = Swarm()

def transfer_to_agent_b():
    return agent_b


agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="Only speak in Haikus.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
)

print(response.messages[-1]["content"])