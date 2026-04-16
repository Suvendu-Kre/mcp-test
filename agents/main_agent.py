from langchain_google_vertexai import ChatVertexAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.tool_manager import calculate

class Agent:
    def __init__(self):
        self.llm = ChatVertexAI(model_name="gemini-2.0-flash-001", project="gen-ai-poc-onboarding", location="us-central1")
        self.tools = [calculate]
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. You can use tools to answer questions."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run(self, message: str) -> str:
        result = self.executor.invoke({"input": message})
        return result["output"]