from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import dotenv, os


dotenv.load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_FILE = os.getenv("OPENAI_API_KEY", "./python_performance_improve.pdf")
QUESTION = os.getenv("QUESTION", "What kind of techniques should i use to improve python performance?")


def get_pdf_pages(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    return pages




embeddings = OpenAIEmbeddings()

faiss_index_file = 'faiss_index'

# Check if the folder exists
if not os.path.exists(faiss_index_file):
    # load pdf file
    pdf_pages = get_pdf_pages(PDF_FILE)
    docs = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)\
        .split_documents(pdf_pages)
    print('Creating FAISS index')
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(faiss_index_file)
else:
    print('Loading FAISS index')
    db = FAISS.load_local(faiss_index_file, embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

model = ChatOpenAI()
from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(model, chain_type="stuff")

question = QUESTION
template = """Answer the question based only on the following context. Include a short summary, a long explanation, page number, chapter title and author name as a reference. If you don't know the answer, just say that you don't know. Don't try to make up an answer.

Context:
{context}

Question: {question}

"""
prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup_and_retrieval | prompt | model | output_parser

print(chain.invoke(QUESTION))

#docs = db.similarity_search(query)
#print(chain.run(input_documents=docs, question=query))