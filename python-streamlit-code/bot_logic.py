import os
import json
from groq import Groq


DEFAULT_MODEL = "llama-3.3-70b-versatile"
COMPANY_NAME = "Visual Builders"
SUPPORT_EMAIL = "buildersvisual@gmail.com"
CONTEXT_FILE = "bot-context.json"


class SupportBot:
    def __init__(self, api_key, model=DEFAULT_MODEL):
        self.client = Groq(api_key=api_key) if api_key else Groq()
        self.model = model
        self.loaded_context = self._load_context()
        self.company_name = (self.loaded_context.get("company", {}).get("name")
                             if self.loaded_context else COMPANY_NAME)
        
        # Build comprehensive system prompt with full bot context
        prompt_parts = [f"You are the friendly customer support assistant for {self.company_name}.\n"]
        
        if self.loaded_context:
            context_json = json.dumps(self.loaded_context, indent=2)
            prompt_parts.append(f"Company Information (JSON):\n{context_json}\n\n")
        
        website = (self.loaded_context.get('contact', {}).get('website', 'https://visualbuilders.in') 
                   if self.loaded_context else 'https://visualbuilders.in')
        
        prompt_parts.extend([
            "Instructions:\n",
            "- You must ONLY answer questions directly related to Visual Builders (our services, pricing, metrics, contact details, FAQs).\n",
            "- STRICTLY refuse to write code, write scripts, solve math problems, answer general knowledge queries, or engage in unrelated chit-chat.\n",
            "- If a query is unrelated to Visual Builders, politely decline, state that you are only programmed to assist with Visual Builders, and offer to help them with the company's services.\n",
            "- Reply like a helpful human in natural conversational messages.\n",
            "- Use information from the company context above to answer accurately.\n",
            "- If unsure, ask one clarifying question.\n",
            f"- If you cannot help with a valid company query, contact human support at {SUPPORT_EMAIL} or visit {website}."
        ])
        self.system_prompt = "".join(prompt_parts)

    def _load_context(self):
        path = os.path.join(os.path.dirname(__file__), CONTEXT_FILE)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_response(self, user_query, chat_history=None):
        return "".join(self.stream_response(user_query, chat_history or []))

    def stream_response(self, user_query, chat_history=None):
        chat_history = chat_history or []
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add history
        for msg in chat_history:
            messages.append(msg)
            
        # Add current query
        messages.append({"role": "user", "content": user_query})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=1,
                max_completion_tokens=256,
                top_p=1,
                stream=True,
                stop=None,
            )

            for chunk in completion:
                yield chunk.choices[0].delta.content or ""
        except Exception as e:
            yield f"Error: {str(e)}"
