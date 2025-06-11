from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

system_prompt_text = '''
Você é um tutor de Inteligência Artificial amigável e experiente.
Explique conceitos de forma clara e concisa, adapte-se ao nível do aluno
e sempre ofereça o próximo passo lógico no aprendizado.
'''

chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=api_key
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    llm=chat,
    tools=[],
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={"prefix": system_prompt_text}
)

def responder_como_tutor(pergunta):
    return agent.run(pergunta)
