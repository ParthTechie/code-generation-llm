import os
from groq import Groq
from config.config import GROQ_API_KEY, GROQ_MODEL

class GroqClient:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL
        self.client = Groq(api_key=self.api_key)
        
    def generate_code(self, prompt, max_tokens=1024, temperature=0.2):
        """
        Generate code based on the given prompt
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert programmer. Generate only code without explanations unless specifically asked for them."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating code: {e}")
            return None