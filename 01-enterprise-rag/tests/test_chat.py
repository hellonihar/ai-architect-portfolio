from django.test import TestCase
from apps.chat.prompts import SYSTEM_PROMPT, CONDENSE_QUESTION_PROMPT, ROUTING_PROMPT


class PromptsTest(TestCase):
    def test_system_prompt_has_context_placeholder(self):
        self.assertIn("{context}", SYSTEM_PROMPT)

    def test_condense_prompt_has_placeholders(self):
        self.assertIn("{chat_history}", CONDENSE_QUESTION_PROMPT)
        self.assertIn("{question}", CONDENSE_QUESTION_PROMPT)

    def test_routing_prompt_has_query_placeholder(self):
        self.assertIn("{query}", ROUTING_PROMPT)
