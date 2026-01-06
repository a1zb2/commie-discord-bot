from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import time
load_dotenv()
video_id = "zPbrkmdcTfo"
try:
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.fetch(video_id)
    transcript = " ".join(chunk.text for chunk in transcript_list)
except TranscriptsDisabled:
    print("No captions available")
splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap = 200)
chunks = splitter.create_documents([transcript])
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
batch_size = 5
vector_store = FAISS.from_documents(chunks[:batch_size], embeddings)
for i in range(batch_size, len(chunks), batch_size):
    time.sleep(3)
    batch = chunks[i : i + batch_size]
    vector_store.add_documents(batch)
retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k":4})
print(retriever.invoke("Who won in the end of the civilization"))
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
prompt = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=['context','question']
)
question = input("Enter your question: ")
retrieved_docs = retriever.invoke(question)
context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
final_prompt = prompt.invoke({"context":context_text,"question":question})
answer = model.invoke(final_prompt)
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
clean = parser.invoke(answer)
print(clean)