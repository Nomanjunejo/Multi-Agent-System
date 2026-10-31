# Multi-Agent Research System

A Gemini-powered AI research automation system built with LangChain. The project uses specialized agents and LLM chains to search the web, extract webpage content, generate structured research reports, and evaluate the final output.

## Features

- **Web Search Agent:** Searches the web for relevant research information.
- **Reader Agent:** Extracts and reads webpage content.
- **Research Writer:** Generates structured and professional research reports.
- **Research Critic:** Evaluates reports, identifies weaknesses, and provides a score.
- **Gemini Integration:** Uses Google's Gemini API for AI-powered reasoning and generation.

## Architecture

User Topic → Search Agent → Reader Agent → Writer Chain → Critic Chain → Final Report

## Tech Stack

- Python
- LangChain
- Google Gemini API
- Tavily Search API
- Python-dotenv

## Project Structure

```text
multi-agent-research-system/
├── agents.py
├── tools.py
├── pipeline.py
├── test_gemini.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-research-system.git
cd multi-agent-research-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run the application

```bash
python pipeline.py
```

## Research Report Structure

The generated report includes:

- Introduction
- Key Findings
- Conclusion
- Sources

The critic evaluates the report and provides strengths, areas for improvement, and an overall score.

## Environment Variables

| Variable | Description |
|---|---|
| GOOGLE_API_KEY | Google Gemini API key |
| TAVILY_API_KEY | Tavily Search API key |

## Future Improvements

- Add a web-based user interface
- Add report export to PDF
- Improve research source verification
- Add iterative critic and writer feedback
- Deploy the application

## License

This project is available under the MIT License.
