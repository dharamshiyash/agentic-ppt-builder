# Agentic AI PowerPoint Builder — Production Version

A multi-agent AI system that automatically generates polished PowerPoint presentations using a team of specialized AI agents orchestrated by LangGraph.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **5-Agent Pipeline** | PlannerAgent → ResearchAgent → WriterAgent → ImageAgent → BuilderAgent |
| **LLM-Powered** | Uses Groq (Llama models) for fast, high-quality content generation |
| **Web Research** | Automatic DuckDuckGo fact-finding to ground content in real data |
| **Image Sourcing** | Unsplash stock photos or DALL-E 3 AI-generated images |
| **Input Validation** | Comprehensive sanitization and constraint checking |
| **Error Handling** | Custom exceptions, graceful degradation, retry logic |
| **Structured Logging** | Rotating file + console logging with agent step tracing |
| **Health Check** | FastAPI `/health` endpoint for monitoring |
| **Caching** | Disk-based caching to avoid redundant LLM calls |
| **Dual Interface** | Streamlit web UI + CLI |

## 🏗️ Architecture

```
production_version/
├── agents/                    # 5 specialized AI agents
│   ├── planner/               # Generates slide outline
│   ├── research/              # Web research per slide
│   ├── writer/                # Writes slide content
│   ├── image/                 # Sources images
│   └── builder/               # Creates .pptx file
├── core/                      # Pipeline infrastructure
│   ├── state.py               # AgentState TypedDict
│   └── graph.py               # LangGraph workflow
├── services/                  # Orchestration layer
│   └── orchestrator.py        # Central pipeline controller
├── config/                    # Application configuration
│   └── settings.py            # Config class with env vars
├── utils/                     # Shared utilities
│   ├── logger.py              # Rotating file + console logging
│   ├── error_handler.py       # Custom exceptions + safe_run
│   └── validators.py          # Input validation + sanitization
├── tools/                     # Agent tools
│   ├── cache.py               # Disk-based function caching
│   ├── retry.py               # Tenacity retry configuration
│   ├── web_search_tool.py     # DuckDuckGo search
│   ├── image_generation_tool.py # DALL-E / Unsplash / placeholder
│   ├── ppt_tool.py            # PPT generation wrapper
│   └── async_queue.py         # Redis queue (optional)
├── tests/                     # Comprehensive test suite
│   ├── test_validators.py     # 25+ input validation tests
│   ├── test_orchestrator.py   # Pipeline orchestration tests
│   ├── test_planner.py        # Planner agent tests
│   ├── test_writer.py         # Writer agent tests
│   ├── test_builder.py        # Builder agent tests
│   ├── test_health.py         # Health check tests
│   ├── test_error_handler.py  # Error handling tests
│   └── test_config.py         # Configuration tests
├── app.py                     # Streamlit web UI
├── main.py                    # CLI entry point
├── health.py                  # FastAPI health endpoint
├── requirements.txt           # Python dependencies
└── .env.example               # Environment variable template
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd production_version
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys:
#   GROQ_API_KEY=your_groq_api_key (required)
#   UNSPLASH_ACCESS_KEY=your_unsplash_key (optional)
#   OPENAI_API_KEY=your_openai_key (optional, for DALL-E images)
```

### 3. Run — Web UI (Streamlit)

```bash
streamlit run app.py
```

### 4. Run — CLI

```bash
python main.py --topic "Artificial Intelligence" --slides 7 --font Calibri --depth Concise
```

### 5. Health Check Server

```bash
python health.py
# → http://localhost:8080/health
# → http://localhost:8080/version
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=term-missing

# Run specific test module
pytest tests/test_validators.py -v
```

## ⚙️ Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | **Required.** Groq API key for LLM access |
| `UNSPLASH_ACCESS_KEY` | — | Optional. For stock photo fetching |
| `OPENAI_API_KEY` | — | Optional. For DALL-E image generation |
| `OUTPUT_DIR` | `outputs` | Where generated .pptx files are saved |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `LOG_DIR` | `logs` | Directory for log files |
| `APP_VERSION` | `1.0.0` | Application version string |

## 🔒 Error Handling

The system uses **graceful degradation** — individual agent failures don't crash the pipeline:

- **LLMError**: Groq API failures → retry with backoff
- **ImageFetchError**: Image API failures → placeholder images
- **FileGenerationError**: PPT creation failures → logged, empty path returned
- **ConfigurationError**: Missing config → clear error messages at startup
- **PipelineTimeoutError**: Execution timeout → pipeline stops, partial results returned

## 📊 Monitoring

- **Logs**: Rotating files in `logs/app.log` (5MB × 5 backups)
- **Health**: `GET /health` returns component status + timestamp
- **Console**: Structured agent step logging with `[AGENT_NAME][STEP]` format

## 🔧 Maintenance

| Task | Frequency | Command / Action |
|------|-----------|------------------|
| **Update Dependencies** | Monthly | `pip install --upgrade -r requirements.txt` |
| **Rotate Logs** | Automatic | RotatingFileHandler keeps 5 × 5MB backups in `logs/` |
| **Clear Cache** | As needed | Delete `.cache/` directory to force fresh LLM calls |
| **Update LLM Model** | Quarterly | Edit `LLM_MODEL` in `config/settings.py` |
| **Review Health** | Continuous | Monitor `GET /health` for `degraded`/`unhealthy` status |
| **Run Tests** | Before deploy | `pytest tests/ -v` — all tests must pass |

> **Tip**: Set up a cron job or CI pipeline to run `pytest tests/ -v` before every deployment.

## 📌 Support Status

| Item | Details |
|------|---------|
| **Current Version** | 1.0.0 |
| **Status** | ✅ Actively Maintained |
| **Python Support** | 3.9+ |
| **Bug Reports** | Open an issue on GitHub |
| **Feature Requests** | Open an issue with `[Feature]` prefix |
| **Security Issues** | Email the maintainer directly |
| **License** | MIT — free for commercial and personal use |

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
