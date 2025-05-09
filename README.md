# Code Generation LLM

A code generation tool built with Streamlit and Groq's LLM API. This project can generate, complete, fix, and translate code in multiple programming languages.

## Features

- ✨ Generate code from natural language descriptions
- 🔄 Complete partial code snippets
- 🐛 Fix bugs in existing code
- 🔀 Translate code between programming languages

## Supported Languages

- Python
- JavaScript
- Java
- C++
- Go

## Project Structure
code-generation-llm/
├── config/
│   └── config.py               # Configuration settings
├── src/
│   ├── api/
│   │   └── groq_client.py      # Groq API client
│   ├── models/
│   │   └── code_generator.py   # Code generation logic
│   └── utils/
│       └── web_ui.py           # Streamlit web UI
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
└── streamlit_app.py            # Streamlit entry point

## Setup

1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Create a `.env` file with your Groq API key: `GROQ_API_KEY=your_key_here`
4. Run the application: `streamlit run streamlit_app.py`

## License
MIT
