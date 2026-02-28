import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

from langchain_core.messages import HumanMessage, AIMessage

model.invoke([HumanMessage(content="Hi! I'm Neel")])
