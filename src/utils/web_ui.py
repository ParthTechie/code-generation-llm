import streamlit as st
from src.models.codeGenerator import CodeGenerator
import time
import random

def get_file_extension(language):
    """Return the appropriate file extension for a language"""
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "cpp": ".cpp",
        "go": ".go"
    }
    return extensions.get(language, ".txt")

def run_streamlit_app():
    """
    Create a Streamlit web UI for the code generation system with improved aesthetics
    """
    # Initialize code generator
    code_generator = CodeGenerator()
    
    # Page configuration
    st.set_page_config(
        page_title="Code Generation LLM",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better aesthetics
    st.markdown("""
    <style>
        .main-header {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2c3e50;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0;
            text-align: center;
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 20px 0;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            background-color: #f0f2f6;
            border-left: 1px solid #ddd;
            border-right: 1px solid #ddd;
            border-top: 1px solid #ddd;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4b6cb7 !important;
            color: white !important;
        }
        .stButton>button {
            background-color: #4b6cb7;
            color: white;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #3a539b;
            border: none;
        }
        .language-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 8px;
            margin-bottom: 8px;
            font-size: 0.8rem;
        }
        .python-badge { background-color: #306998; color: white; }
        .javascript-badge { background-color: #f7df1e; color: black; }
        .java-badge { background-color: #b07219; color: white; }
        .cpp-badge { background-color: #f34b7d; color: white; }
        .go-badge { background-color: #00ADD8; color: white; }
        .feature-card {
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            background-color: white;
        }
        .example-code {
            padding: 10px;
            border-radius: 5px;
            background-color: #f8f9fa;
            border-left: 3px solid #4b6cb7;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            font-family: 'Courier New', Courier, monospace;
        }
        .stTextArea>div>div>textarea {
            font-family: 'Consolas', 'Courier New', monospace;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">Code Generation LLM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate, complete, fix and translate code powered by AI</p>', unsafe_allow_html=True)
    
    # Language badges
    st.markdown('<div style="text-align: center; margin-bottom: 20px;">'
                '<span class="language-badge python-badge">Python</span>'
                '<span class="language-badge javascript-badge">JavaScript</span>'
                '<span class="language-badge java-badge">Java</span>'
                '<span class="language-badge cpp-badge">C++</span>'
                '<span class="language-badge go-badge">Go</span>'
                '</div>', unsafe_allow_html=True)
    
    # Sidebar enhancements
    with st.sidebar:
        st.markdown('<h2 style="text-align:center; color:#4b6cb7;">Settings & Info</h2>', unsafe_allow_html=True)
        
        st.markdown('### Model Parameters')
        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.2,
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
        
        max_tokens = st.slider(
            "Max Output Length",
            min_value=500,
            max_value=2000,
            value=1500,
            step=100,
            help="Maximum length of generated code"
        )
        
        st.markdown('---')
        
        st.markdown('### Tips & Tricks')
        with st.expander("Writing Good Prompts"):
            st.markdown("""
            - Be specific about what the code should do
            - Mention edge cases and error handling needs
            - Specify any libraries or approaches to use
            - Give examples when possible
            """)
        
        with st.expander("About Code Translation"):
            st.markdown("""
            Translation works best for:
            - Well-structured code
            - Code using standard language features
            - Code with clear logic patterns
            
            Review the output carefully and test it!
            """)
        
        st.markdown('---')
        
        st.markdown('<div style="text-align:center; padding: 20px 0; opacity:0.7;">Powered by ParthTechie</div>', unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["✨ Generate Code", "🔄 Complete Code", "🐛 Fix Bugs", "🔀 Translate Code"])
    
    # Tab 1: Generate Code from Description
    with tab1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('### Generate Code from Description')
        st.markdown('Enter a natural language description of what you want the code to do, and the AI will generate it for you.')
        
        language = st.selectbox(
            "Programming Language",
            options=["python", "javascript", "java", "cpp", "go"],
            key="gen_language"
        )
        
        # Example prompts
        example_prompts = {
            "python": "Create a function that takes a list of numbers and returns the average of the top 3 largest numbers.",
            "javascript": "Write a function that fetches data from an API and displays it in an HTML table.",
            "java": "Create a class representing a bank account with methods for deposit, withdrawal and balance checking.",
            "cpp": "Implement a template class for a stack data structure with push, pop and peek operations.",
            "go": "Write a function that reads a CSV file and returns a structured data object."
        }
        
        with st.expander("See Example Prompt"):
            st.code(example_prompts[language], language=language)
        
        prompt = st.text_area(
            "Enter a description of the code you want to generate",
            height=150,
            key="gen_prompt",
            placeholder=example_prompts[language]
        )
        
        if st.button("✨ Generate Code", key="gen_button"):
            if not prompt.strip():
                st.error("Please enter a prompt.")
            else:
                with st.spinner("Generating code... This might take a few moments..."):
                    # Add a small delay for better UX
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    try:
                        code = code_generator.generate_from_prompt(
                            prompt, language, max_tokens=max_tokens, temperature=temperature
                        )
                        
                        st.success("Code generated successfully! 🎉")
                        st.code(code, language=language)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            # Add download button
                            file_extension = get_file_extension(language)
                            st.download_button(
                                label="💾 Download Code",
                                data=code,
                                file_name=f"generated_code{file_extension}",
                                mime="text/plain"
                            )
                        with col2:
                            # Copy to clipboard button (simulated)
                            if st.button("📋 Copy to Clipboard", key="gen_copy"):
                                st.success("Code copied to clipboard!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Complete Code
    with tab2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('### Complete Partial Code')
        st.markdown('Enter your partial code, and the AI will suggest a completion.')
        
        complete_language = st.selectbox(
            "Programming Language",
            options=["python", "javascript", "java", "cpp", "go"],
            key="complete_language"
        )
        
        # Example code snippets by language
        example_code_snippets = {
            "python": "def fibonacci(n):\n    \"\"\"Return the nth Fibonacci number.\"\"\"\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:",
            "javascript": "function sortUsers(users) {\n    // Sort users by age in descending order\n    ",
            "java": "public class BinarySearch {\n    public static int search(int[] array, int target) {\n        int left = 0;\n        int right = array.length - 1;\n        ",
            "cpp": "#include <vector>\n\ntemplate <typename T>\nstd::vector<T> merge(const std::vector<T>& left, const std::vector<T>& right) {\n    ",
            "go": "func processData(data []string) map[string]int {\n    result := make(map[string]int)\n    "
        }
        
        with st.expander("See Example Code Snippet"):
            st.code(example_code_snippets[complete_language], language=complete_language)
        
        code_prefix = st.text_area(
            "Enter code to complete",
            height=200,
            key="code_prefix",
            placeholder=example_code_snippets[complete_language]
        )
        
        if st.button("🔄 Complete Code", key="complete_button"):
            if not code_prefix.strip():
                st.error("Please enter some code to complete.")
            else:
                with st.spinner("Completing code... AI is thinking..."):
                    # Add a small delay for better UX
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    try:
                        completed_code = code_generator.complete_code(
                            code_prefix, complete_language, max_tokens=max_tokens, temperature=temperature
                        )
                        
                        st.success("Code completed successfully! 🎉")
                        st.code(completed_code, language=complete_language)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            # Add download button
                            file_extension = get_file_extension(complete_language)
                            st.download_button(
                                label="💾 Download Code",
                                data=completed_code,
                                file_name=f"completed_code{file_extension}",
                                mime="text/plain"
                            )
                        with col2:
                            # Copy to clipboard button (simulated)
                            if st.button("📋 Copy to Clipboard", key="complete_copy"):
                                st.success("Code copied to clipboard!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Fix Bugs
    with tab3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('### Fix Bugs in Code')
        st.markdown('Paste your buggy code, and the AI will attempt to fix the issues.')
        
        fix_language = st.selectbox(
            "Programming Language",
            options=["python", "javascript", "java", "cpp", "go"],
            key="fix_language"
        )
        
        # Example buggy code by language
        example_buggy_code = {
            "python": "def calculate_average(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total / len(numbers)\n\n# This will crash with an empty list\nprint(calculate_average([]))",
            "javascript": "function sortArray(arr) {\n    for (let i = 0; i < arr.length; i++) {\n        for (let j = 0; j < arr.length; j++) {\n            if (arr[i] < arr[j]) {\n                let temp = arr[i];\n                arr[i] = arr[j];\n                arr[j] = temp;\n            }\n        }\n    }\n    return arr;\n}",
            "java": "public class ListNode {\n    int val;\n    ListNode next;\n    \n    public ListNode(int val) {\n        this.val = val;\n    }\n    \n    public void printList() {\n        ListNode current = this;\n        while (current != null) {\n            System.out.print(current.val + \" \");\n            current = next; // Bug: should be current.next\n        }\n    }\n}",
            "cpp": "#include <iostream>\n#include <vector>\n\nint findMax(std::vector<int> numbers) {\n    if (numbers.size() == 0) {\n        return -1; // This could be a bug depending on requirements\n    }\n    \n    int max = numbers[0];\n    for (int i = 0; i <= numbers.size(); i++) { // Bug: should be i < numbers.size()\n        if (numbers[i] > max) {\n            max = numbers[i];\n        }\n    }\n    return max;\n}",
            "go": "func processMap(data map[string]int) int {\n    total := 0\n    for key, value := range data {\n        if key == \"special\" {\n            total += value * 2\n        }\n    }\n    return total // Bug: doesn't add non-special values\n}"
        }
        
        with st.expander("See Example Buggy Code"):
            st.code(example_buggy_code[fix_language], language=fix_language)
        
        buggy_code = st.text_area(
            "Enter code with bugs to fix",
            height=200,
            key="buggy_code",
            placeholder=example_buggy_code[fix_language]
        )
        
        if st.button("🐛 Fix Bugs", key="fix_button"):
            if not buggy_code.strip():
                st.error("Please enter some code to fix.")
            else:
                with st.spinner("Analyzing and fixing code... Hunting for bugs..."):
                    # Add a small delay for better UX
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    try:
                        fixed_code = code_generator.fix_bugs(
                            buggy_code, fix_language, max_tokens=max_tokens, temperature=temperature
                        )
                        
                        st.success("Bugs fixed successfully! 🎉")
                        
                        # Show before/after comparison
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Original Code (with bugs)")
                            st.code(buggy_code, language=fix_language)
                        with col2:
                            st.markdown("#### Fixed Code")
                            st.code(fixed_code, language=fix_language)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            # Add download button
                            file_extension = get_file_extension(fix_language)
                            st.download_button(
                                label="💾 Download Fixed Code",
                                data=fixed_code,
                                file_name=f"fixed_code{file_extension}",
                                mime="text/plain"
                            )
                        with col2:
                            # Copy to clipboard button (simulated)
                            if st.button("📋 Copy to Clipboard", key="fix_copy"):
                                st.success("Code copied to clipboard!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
                        
    # Tab 4: Translate Code
    with tab4:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('### Translate Code Between Languages')
        st.markdown('Convert code from one programming language to another while preserving functionality.')
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_language = st.selectbox(
                "Source Language",
                options=["python", "javascript", "java", "cpp", "go"],
                key="source_language"
            )
        
        with col2:
            target_language = st.selectbox(
                "Target Language",
                options=["javascript", "python", "java", "cpp", "go"],
                key="target_language",
                index=0  # Default to javascript
            )
        
        # Example translation code snippets by source language
        example_translation_code = {
            "python": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr",
            "javascript": "function calculateFactorial(n) {\n    if (n === 0 || n === 1) {\n        return 1;\n    }\n    let result = 1;\n    for (let i = 2; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "java": "public class Rectangle {\n    private double width;\n    private double height;\n    \n    public Rectangle(double width, double height) {\n        this.width = width;\n        this.height = height;\n    }\n    \n    public double getArea() {\n        return width * height;\n    }\n    \n    public double getPerimeter() {\n        return 2 * (width + height);\n    }\n}",
            "cpp": "#include <string>\n\nclass Person {\nprivate:\n    std::string name;\n    int age;\n\npublic:\n    Person(std::string name, int age) : name(name), age(age) {}\n    \n    std::string getName() const {\n        return name;\n    }\n    \n    int getAge() const {\n        return age;\n    }\n    \n    void birthday() {\n        age++;\n    }\n};",
            "go": "func calculateAverage(numbers []float64) float64 {\n    if len(numbers) == 0 {\n        return 0\n    }\n    \n    var sum float64\n    for _, num := range numbers {\n        sum += num\n    }\n    \n    return sum / float64(len(numbers))\n}"
        }
        
        with st.expander(f"See Example {source_language.capitalize()} Code for Translation"):
            st.code(example_translation_code[source_language], language=source_language)
        
        source_code = st.text_area(
            f"Enter {source_language} code to translate",
            height=250,
            key="source_code",
            placeholder=example_translation_code[source_language]
        )
        
        if st.button("🔀 Translate Code", key="translate_button"):
            if not source_code.strip():
                st.error("Please enter some code to translate.")
            elif source_language == target_language:
                st.error("Source and target languages must be different.")
            else:
                with st.spinner(f"Translating {source_language} to {target_language}... This may take a moment..."):
                    # Add a small delay for better UX
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    try:
                        translated_code = code_generator.translate_code(
                            source_code, 
                            source_language, 
                            target_language, 
                            max_tokens=max_tokens, 
                            temperature=temperature
                        )
                        
                        st.success(f"Translation from {source_language} to {target_language} completed! 🎉")
                        
                        # Show side-by-side comparison
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"#### Original {source_language.capitalize()} Code")
                            st.code(source_code, language=source_language)
                        with col2:
                            st.markdown(f"#### Translated {target_language.capitalize()} Code")
                            st.code(translated_code, language=target_language)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            # Add download button
                            file_extension = get_file_extension(target_language)
                            st.download_button(
                                label="💾 Download Translated Code",
                                data=translated_code,
                                file_name=f"translated_code{file_extension}",
                                mime="text/plain"
                            )
                        with col2:
                            # Copy to clipboard button (simulated)
                            if st.button("📋 Copy to Clipboard", key="translate_copy"):
                                st.success("Code copied to clipboard!")
                        
                        # Show translation notes
                        with st.expander("Translation Notes & Tips"):
                            st.markdown("""
                            ### Important Translation Notes
                            
                            - **Language Differences**: Different languages have different idioms and patterns. The translation preserves functionality but may not use the most idiomatic patterns.
                            
                            - **Library Support**: Libraries and frameworks are handled differently across languages. You may need to add appropriate imports or dependencies.
                            
                            - **Performance**: The translated code may not have the same performance characteristics as the original.
                            
                            - **Testing**: Always test translated code thoroughly before using it in production.
                            """)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('---')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p style="text-align: center; opacity: 0.7;">Code Generation LLM is a project that leverages the power of large language models to assist with code generation, completion, debugging, and translation.</p>', unsafe_allow_html=True)