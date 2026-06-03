SYSTEM_PROMPT = """You are an enterprise RAG assistant. Answer the user's question using only the provided context.
If the context does not contain enough information, say so clearly.
Always cite the source document IDs for each piece of information you use.

Context:
{context}
"""

CONDENSE_QUESTION_PROMPT = """Given the following conversation history and a follow-up question,
rephrase the follow-up question to be a standalone question.

Chat History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""

ROUTING_PROMPT = """Classify the following user query into one of these categories:
- retrieval: needs document search
- general: general knowledge question
- summarization: needs document summarization
- chitchat: casual conversation

Query: {query}

Category:"""
