import os
try:
    import openai
except Exception:
    openai = None
from dotenv import load_dotenv
import re

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class GPTAgent:
    def __init__(self, memory):
        self.memory = memory
        self.tools = {}

        # Configure OpenAI if key present
        if OPENAI_API_KEY and openai is not None:
            openai.api_key = OPENAI_API_KEY

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def _call_openai(self, prompt, model='gpt-3.5-turbo'):
        # Lightweight call; use try/except to avoid crashing
        if openai is None:
            return self._simulate_response(prompt)
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[{'role':'user','content':prompt}],
                max_tokens=200,
                temperature=0.7
            )
            return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"[Simulated GPT fallback due to error: {str(e)}] {self._simulate_response(prompt)}"

    def _simulate_response(self, prompt):
        # Very basic rule-based fallback
        low = prompt.lower()
        if 'summarize' in low:
            words = prompt.split()
            return 'Summary: ' + ' '.join(words[:20]) + ('...' if len(words) > 20 else '')
        if 'joke' in low:
            return 'Why did the neural network cross the road? To get to the other layer!'
        if 'weather' in low:
            return 'Simulated weather: 20°C, Clear.'
        return "I'm a simulated agent. Provide a clearer prompt or set OPENAI_API_KEY to get real GPT responses."

    def _use_tool(self, user_input):
        # Tool invocation: if tool name appears in input, use it
        for name, tool in self.tools.items():
            if re.search(rf"\b{name}\b", user_input, flags=re.IGNORECASE):
                try:
                    return tool.run(user_input)
                except Exception as e:
                    return f"Tool '{name}' error: {e}"
        return None

    def handle(self, user_input):
        # save to memory
        try:
            self.memory.add({'user': user_input})
        except Exception:
            pass
        # check tools first
        tool_result = self._use_tool(user_input)
        if tool_result:
            try:
                self.memory.add({'agent': tool_result})
            except Exception:
                pass
            return tool_result

        # otherwise call GPT if key exists, else simulate
        if OPENAI_API_KEY and openai is not None:
            prompt = f"You are an assistant. User said: {user_input}"
            resp = self._call_openai(prompt)
        else:
            resp = self._simulate_response(user_input)
        try:
            self.memory.add({'agent': resp})
        except Exception:
            pass
        return resp
