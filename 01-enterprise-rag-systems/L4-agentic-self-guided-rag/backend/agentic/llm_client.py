import json
import logging
import re

from core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self._llm = None
        self._init_llm()

    def _init_llm(self):
        if not settings.groq_api_key:
            logger.warning("No GROQ_API_KEY set. LLM calls will use fallback responses.")
            return
        try:
            from langchain_groq import ChatGroq
            self._llm = ChatGroq(
                model=settings.groq_model,
                temperature=settings.groq_temperature,
                api_key=settings.groq_api_key,
            )
            logger.info("LLM initialized: %s", settings.groq_model)
        except Exception as e:
            logger.warning("LLM init failed: %s. Using fallback.", e)

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        if self._llm is None:
            return ""

        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = self._llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            logger.error("LLM call failed: %s", e)
            return ""

    def _parse_json(self, text: str) -> dict:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return {}

    def should_retrieve(self, query: str, context: str = "") -> dict:
        system = (
            "You are a retrieval decision system. Given a user query, decide whether retrieval "
            "from a knowledge base is needed to answer it correctly.\n\n"
            "Respond in JSON with exactly these keys:\n"
            '  "retrieve": true/false (whether retrieval is needed)\n'
            '  "reason": string (brief explanation)\n'
            '  "confidence": float (0-1)'
        )
        user = f"Query: {query}\n" + (f"Conversation context: {context}\n" if context else "")
        raw = self._call_llm(system, user)
        if not raw:
            return {"retrieve": True, "reason": "Default: retrieval needed", "confidence": 0.5}
        return self._parse_json(raw)

    def check_relevance(self, query: str, passage: str) -> dict:
        system = (
            "You are a relevance checker. Determine how relevant the given passage is to the query.\n\n"
            'Respond in JSON with:\n'
            '  "label": one of "relevant", "partial", "irrelevant"\n'
            '  "confidence": float (0-1)\n'
            '  "explanation": string (brief reason)'
        )
        user = f"Query: {query}\n\nPassage: {passage[:2000]}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"label": "relevant", "confidence": 0.5, "explanation": "Default: assumed relevant"}
        return self._parse_json(raw)

    def check_citation(self, statement: str, passage: str) -> dict:
        system = (
            "You are a citation verifier. Determine whether the given statement is factually supported by the passage.\n\n"
            'Respond in JSON with:\n'
            '  "label": one of "supported", "partial", "unsupported"\n'
            '  "confidence": float (0-1)\n'
            '  "explanation": string (brief reason)'
        )
        user = f"Statement: {statement}\n\nPassage: {passage[:2000]}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"label": "supported", "confidence": 0.5, "explanation": "Default: assumed supported"}
        return self._parse_json(raw)

    def score_quality(self, query: str, passages: list[str]) -> dict:
        system = (
            "You are a retrieval quality assessor. Evaluate how well the retrieved passages answer the query.\n\n"
            'Respond in JSON with:\n'
            '  "quality": one of "high", "medium", "low"\n'
            '  "confidence": float (0-1)\n'
            '  "explanation": string (brief reason)'
        )
        passages_text = "\n\n".join(f"[{i+1}] {p[:500]}" for i, p in enumerate(passages))
        user = f"Query: {query}\n\nRetrieved passages:\n{passages_text}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"quality": "medium", "confidence": 0.5, "explanation": "Default: assumed medium"}
        return self._parse_json(raw)

    def classify_complexity(self, query: str) -> dict:
        system = (
            "You are a query complexity classifier. Given a user query, classify its complexity level.\n\n"
            '- "simple": factoid, definition, single-concept (can answer without retrieval)\n'
            '- "moderate": explanation, comparison, single-step reasoning (benefits from one retrieval pass)\n'
            '- "complex": multi-step reasoning, multi-concept synthesis, analysis (needs iterative retrieval)\n\n'
            'Respond in JSON with:\n'
            '  "complexity": "simple" | "moderate" | "complex"\n'
            '  "confidence": float (0-1)\n'
            '  "explanation": string (brief reason)'
        )
        user = f"Query: {query}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"complexity": "moderate", "confidence": 0.5, "explanation": "Default: moderate"}
        return self._parse_json(raw)

    def decompose_query(self, query: str) -> dict:
        system = (
            "You are a query decomposition system. Break down complex queries into simpler sub-questions "
            "that can be answered independently and then combined.\n\n"
            'Respond in JSON with:\n'
            '  "sub_questions": list of strings (the sub-questions, max 5)\n'
            '  "synthesis_instruction": string (how to combine answers)\n'
            '  "explanation": string'
        )
        user = f"Query: {query}"
        raw = self._call_llm(system, user)
        if not raw:
            return {
                "sub_questions": [query],
                "synthesis_instruction": "Answer the original question directly.",
                "explanation": "Default: no decomposition",
            }
        result = self._parse_json(raw)
        if "sub_questions" not in result:
            result["sub_questions"] = [query]
        return result

    def generate_answer(self, query: str, passages: list, instruction: str = "") -> dict:
        system = (
            "You are a helpful assistant that answers questions based on the provided passages. "
            "Use only the information in the passages to answer. If the passages do not contain enough information, say so.\n"
            "Cite specific passages by their source document ID if available.\n\n"
            "Provide your answer in this JSON structure:\n"
            '  "answer": string (your response)\n'
            '  "citations": list of strings (document IDs referenced)\n'
            '  "confidence": float (0-1)'
        )

        def _get_id(p):
            return p.id if hasattr(p, "id") else p.get("id", "?")
        def _get_content(p, n=1500):
            return p.content[:n] if hasattr(p, "content") else p["content"][:n]

        passages_text = "\n\n".join(f"[{_get_id(p)}] {_get_content(p)}" for p in passages)
        user = f"Question: {query}\n\n"
        if instruction:
            user += f"Instructions: {instruction}\n\n"
        user += f"Passages:\n{passages_text}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"answer": "I could not generate an answer.", "citations": [], "confidence": 0.0}
        result = self._parse_json(raw)
        if "answer" not in result:
            result["answer"] = raw
        if "citations" not in result:
            result["citations"] = []
        return result

    def generate_direct(self, query: str) -> dict:
        system = (
            "You are a knowledgeable assistant. Answer the user's question using your existing knowledge. "
            "If you are not sure, say so rather than making up information.\n\n"
            'Respond in JSON with:\n'
            '  "answer": string (your response)\n'
            '  "confidence": float (0-1)'
        )
        user = f"Question: {query}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"answer": "I don't have enough information to answer that.", "confidence": 0.0}
        result = self._parse_json(raw)
        if "answer" not in result:
            result["answer"] = raw
        return result

    def synthesize_answers(self, original_query: str, sub_answers: list[dict]) -> str:
        system = (
            "You are a synthesis assistant. Combine the answers to sub-questions into a comprehensive "
            "response to the original query. Ensure the final answer is coherent, non-redundant, "
            "and directly addresses the original question."
        )
        parts = [f"Sub-question {i+1}: {a['question']}\nAnswer: {a['answer']}" for i, a in enumerate(sub_answers)]
        user = f"Original query: {original_query}\n\nSub-answers:\n" + "\n\n".join(parts)
        raw = self._call_llm(system, user)
        return raw or "I could not synthesize the answers."

    def select_strategy(self, query: str) -> str:
        system = (
            "You are a strategy selector for an agentic RAG system. Given a user query, select the best "
            "agentic strategy from: 'self_rag', 'corrective_rag', 'adaptive_rag', 'multi_hop'.\n\n"
            '- self_rag: when the query may or may not need retrieval, reflection is important\n'
            '- corrective_rag: when retrieval quality is uncertain, need fallback mechanisms\n'
            '- adaptive_rag: when query complexity varies, need to choose between simple/complex paths\n'
            '- multi_hop: when the query requires connecting information across multiple documents\n\n'
            'Respond in JSON with:\n'
            '  "strategy": string\n'
            '  "explanation": string'
        )
        user = f"Query: {query}"
        raw = self._call_llm(system, user)
        if not raw:
            return "self_rag"
        result = self._parse_json(raw)
        strategy = result.get("strategy", "self_rag")
        valid = {"self_rag", "corrective_rag", "adaptive_rag", "multi_hop"}
        return strategy if strategy in valid else "self_rag"

    def reflect_completeness(self, query: str, answer: str) -> dict:
        system = (
            "You are a completeness checker. Determine whether the given answer fully and accurately answers the query.\n\n"
            'Respond in JSON with:\n'
            '  "complete": true/false\n'
            '  "confidence": float (0-1)\n'
            '  "follow_up": string or null (a follow-up question if incomplete)'
        )
        user = f"Query: {query}\n\nAnswer: {answer}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"complete": True, "confidence": 0.5, "follow_up": None}
        return self._parse_json(raw)

    def rewrite_query(self, query: str, passages: list[str]) -> dict:
        system = (
            "You are a query rewriter. The initial retrieval for the given query did not return high-quality results. "
            "Rewrite the query to improve retrieval. Use the poor results to understand what went wrong.\n\n"
            'Respond in JSON with:\n'
            '  "rewritten_query": string\n'
            '  "explanation": string'
        )
        passages_text = "\n\n".join(p[:500] for p in passages[:3])
        user = f"Original query: {query}\n\nPoor results:\n{passages_text}"
        raw = self._call_llm(system, user)
        if not raw:
            return {"rewritten_query": query, "explanation": "Default: no rewrite"}
        return self._parse_json(raw)

    @property
    def is_available(self) -> bool:
        return self._llm is not None
