from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate(
    template= "Answer the following question about {topic}: {question}",
    input_variables=["topic", "question"]
)
chain = prompt | model | parser
print(chain.invoke({"topic": "space exploration", "question": "What was the first satellite launched into space?"}))