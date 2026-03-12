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
| **Safety Guardrails** | Pre-pipeline prompt safety check blocks harmful topics |
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
│   └── validators.py          # Input validation + safety guardrails
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
│   ├── test_config.py         # Configuration tests
│   └── test_safety.py         # Safety guardrail tests
├── .streamlit/
│   └── config.toml            # Streamlit deployment config
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

## 🛡️ Safety Guardrails

All topics are screened by `check_prompt_safety()` **before** any agent is invoked. The guardrail blocks:

- Illegal activities (drug synthesis, hacking guides, trafficking)
- Explicit violence (murder/torture instructions)
- Self-harm and exploitation content
- Terrorism and extremism promotion

If a topic is flagged, a `ValueError` is raised immediately and the pipeline is not started. The Streamlit UI displays a clear "Content Safety Error" message.

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

## ⚖️ Alternative Solutions Comparison

| Approach | Time Required | Quality | Customization | AI-Powered | Research |
|----------|:---:|:---:|:---:|:---:|:---:|
| **Manual PPT creation** | Hours | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | Manual |
| **Single LLM prompt** | Minutes | ⭐⭐⭐ | ⭐⭐ | ✅ | None |
| **Template-based tools** (Canva, Gamma) | 15–30 min | ⭐⭐⭐⭐ | ⭐⭐⭐ | Partial | None |
| **Agentic Multi-Agent System** *(this)* | ~2 min | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Full | ✅ Auto |

**Why agentic?** Each agent specializes in one task — planning, research, writing, image sourcing, and building. This division produces significantly higher-quality output than a single monolithic LLM call, while keeping generation time under 2 minutes.

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| **Average generation time** | ~90–120 seconds (end-to-end) |
| **Number of AI agents** | 5 (Planner, Research, Writer, Image, Builder) |
| **Automated tests** | 90+ across 9 test modules |
| **Supported slide range** | 1–20 slides per presentation |
| **LLM model** | Llama 3.3 70B Versatile (via Groq) |
| **Cache hit speedup** | ~5–10× faster on repeated topics |
| **Retry attempts** | Up to 3 per API call with exponential backoff |
| **Log retention** | 5 rotating files × 5MB = up to 25MB |

## 🖥️ UX Design

### Streamlit Interface Layout

The web UI is organized into two areas:

**Sidebar (left)**
- Live status badges for each API key (GROQ, Unsplash, OpenAI)
- Agent pipeline overview with emoji icons for each step
- App version display

**Main area (right)**
- Single text input for the presentation topic (max 200 chars)
- Two-column layout: slide count + font on the left, depth + spacer on the right
- One-click "🚀 Generate Presentation" button
- Live status panel showing real-time agent progress
- Download button appears immediately when the `.pptx` is ready

### Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Minimal input** | Only 4 parameters required — topic, slides, font, depth |
| **Clear feedback** | Each agent step is logged visibly in the UI status panel |
| **Error transparency** | Validation, safety, and system errors shown with distinct icons |
| **Graceful degradation** | Missing optional API keys shown as warnings, not blockers |
| **Readable defaults** | Calibri font, 7 slides, Concise depth — sensible for most topics |

### Font & Readability

- Default font: **Calibri** — clean, professional, widely supported in PowerPoint
- Body text: 22pt for readability on projected slides
- Title text: 36–44pt bold for clear hierarchy
- All text uses RGB black `(0, 0, 0)` against white slide backgrounds

## 📜 License

This project is licensed under the **MIT License**, which means you are free to:

- ✅ Use it commercially
- ✅ Modify and distribute it
- ✅ Include it in private projects

The only requirement is that the original copyright notice and license text are included in any copy or substantial portion of the software.

See the [LICENSE](LICENSE) file for the full license text.
