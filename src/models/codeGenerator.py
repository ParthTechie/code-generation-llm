from src.api.groqClient import GroqClient
from config.config import GROQ_MODEL
import re

class CodeGenerator:
    def __init__(self, model=GROQ_MODEL):
        self.groq_client = GroqClient(model=model)
        self.model = model
    
    def clean_code(self, code_text):
        """Remove markdown code blocks and language identifiers from the code"""
        # Remove markdown code blocks
        code_text = re.sub(r'```\w*\n', '', code_text)
        code_text = re.sub(r'```', '', code_text)
        
        # Remove any leading/trailing whitespace
        code_text = code_text.strip()
        
        return code_text
        
    def generate_from_prompt(self, prompt, language="python", max_tokens=1024, temperature=0.2):
        """
        Generate code from a natural language prompt
        """
        enhanced_prompt = f"""
        Generate {language} code for the following task:
        
        {prompt}
        
        Return only the raw code without explanations, markdown formatting, or triple backticks.
        """
        
        code = self.groq_client.generate_code(enhanced_prompt, max_tokens, temperature)
        return self.clean_code(code)
    
    def complete_code(self, code_prefix, language="python", max_tokens=1024, temperature=0.2):
        """
        Complete partially written code
        """
        enhanced_prompt = f"""
        Complete the following {language} code:
        
        {code_prefix}
        
        Return only the completed code without markdown formatting, triple backticks, or explanations.
        """
        
        completion = self.groq_client.generate_code(enhanced_prompt, max_tokens, temperature)
        cleaned_completion = self.clean_code(completion)
        
        # Check if the completion already includes the prefix
        if code_prefix in cleaned_completion:
            return cleaned_completion
        
        return code_prefix + "\n" + cleaned_completion
    
    def fix_bugs(self, buggy_code, language="python", max_tokens=1024, temperature=0.2):
        """
        Fix bugs in the provided code
        """
        enhanced_prompt = f"""
        Fix the bugs in the following {language} code:
        
        {buggy_code}
        
        Return only the fixed code without markdown formatting, triple backticks, or explanations.
        """
        
        code = self.groq_client.generate_code(enhanced_prompt, max_tokens, temperature)
        return self.clean_code(code)
    
    def generate_tests(self, function_code, language="python", max_tokens=1024, temperature=0.2):
        """
        Generate unit tests for a given function
        """
        enhanced_prompt = f"""
        Generate unit tests for the following {language} function:
        
        {function_code}
        
        Return only the test code without markdown formatting, triple backticks, or explanations.
        """
        
        code = self.groq_client.generate_code(enhanced_prompt, max_tokens, temperature)
        return self.clean_code(code)
    
    def translate_code(self, source_code, source_language="python", target_language="javascript", max_tokens=1500, temperature=0.2):
        """
        Translate code from one programming language to another while preserving functionality
        
        Args:
            source_code (str): The source code to translate
            source_language (str): The language of the source code
            target_language (str): The language to translate the code to
            max_tokens (int): Maximum tokens to generate
            temperature (float): Controls randomness
            
        Returns:
            str: Translated code
        """
        enhanced_prompt = f"""
        Translate the following {source_language} code to {target_language}, preserving exactly the same functionality and behavior:
        
        {source_code}
        
        Return only the translated {target_language} code without markdown formatting, triple backticks, or explanations.
        """
        
        code = self.groq_client.generate_code(enhanced_prompt, max_tokens, temperature)
        return self.clean_code(code)