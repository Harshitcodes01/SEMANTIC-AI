AI Orchestrator – Semantic Intelligence Engine



Overview
The AI Orchestrator is a modular intelligence system that transforms natural language inputs into structured, simulation-ready scientific outputs (spec.json).
It integrates hybrid parsing, vector-based retrieval, research enrichment, and strict validation into a unified pipeline.
This system acts as the core reasoning layer of the Prana-G AI pipeline, enabling downstream simulation systems to operate on reliable, structured data.

Core Capabilities

Hybrid parsing (rules + LLM) for high accuracy
Semantic retrieval using vector embeddings
Trait-to-mechanism scientific mapping
Strict schema validation using Pydantic
Retry and fallback mechanisms for robustness
Modular architecture for scalability



Architecture
User Input   ↓Hybrid Parser (Rules + LLM)   ↓Vector Search (ChromaDB + Embeddings)   ↓Research Layer (Trait → Mechanism)   ↓Spec Generator   ↓Pydantic Validator   ↓Final spec.json
Workflow Execution
Parse → Search → Research → Generate → Validate

Parsing extracts structured intent

Search retrieves relevant traits
Research adds scientific reasoning

Generator builds final spec
Validator ensures correctness



Semantic-AI/
│
├── main.py                # Entry point (CLI pipeline)
├── workflow.py            # LangGraph workflow orchestration
├── llm_parser.py          # Hybrid parsing system
├── vector_search.py       # ChromaDB-based semantic retrieval
├── research.py            # Scientific insight mapping
├── spec_generator.py      # Final JSON generation logic
├── validator.py           # Pydantic validation layer
├── models.py              # Schema definitions
├── app.py                 # Streamlit UI (optional)
└── requirements.txt

Example Input
rice in hot dry climate

Example Output
{  "crop": "rice",  "location": "hot dry climate",  "temperature": 25,  "stress": ["heat", "drought"],  "traits": [    "deep root system",    "heat shock protein expression"  ],  "scientific_basis": [    "Improves water uptake from deeper soil layers",    "Stabilizes proteins under heat stress"  ],  "confidence": 0.85}

Installation
git clone https://github.com/your-username/semantic-ai.gitcd semantic-aipython -m venv venvvenv\Scripts\activatepip install -r requirements.txt

Usage
CLI
python main.py

Streamlit UI
streamlit run app.py


Tech Stack

Python
LangGraph
Sentence Transformers
ChromaDB
Pydantic
Streamlit
Ollama (Llama3)



Design Principles


Reliability — validation + retry logic
Scalability — vector database integration
Modularity — independent components

Explainability — scientific reasoning layer
Performance — optimized execution pipeline



Performance Highlights


Reduced hallucinations using hybrid parsing
Context-aware retrieval using metadata filtering
Structured output with strict schema validation
Fault-tolerant pipeline with retry handling





Future Roadmap


Integration with Semantic Scholar / ArXiv APIs

FastAPI deployment for production

Async execution for low latency

Large-scale trait ingestion (Parquet + vector DB)

Advanced ranking and scoring models


Contribution
Developed as part of the Prana-G AI system, focusing on building the core orchestration and intelligence layer.

License
MIT License



👨‍💻 Author

Harshit



