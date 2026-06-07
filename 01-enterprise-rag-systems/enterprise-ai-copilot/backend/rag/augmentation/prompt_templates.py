from langchain_core.prompts import ChatPromptTemplate

RAG_SYSTEM_PROMPT = """You are an AI assistant that answers questions based on the provided context.
Use only the information in the context to answer. If the context doesn't contain enough information, say so.
Cite your sources when referencing specific information.

Context:
{context}"""

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", "{query}")
])

CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Given the conversation history, rephrase the user's question to be standalone."),
    ("human", "Conversation history:\n{history}\n\nQuestion: {query}")
])
