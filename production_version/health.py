"""
Health Check Endpoint
---------------------
Provides a lightweight health monitoring endpoint for the Agentic PPT Builder.
Can be run as a standalone FastAPI server or imported as a module.

Endpoints:
    GET /health   — Returns system health status
    GET /version  — Returns application version info

Usage (standalone):
    python health.py

Usage (import):
    from health import check_health
    status = check_health()
"""

import os
import sys
import importlib
from datetime import datetime, timezone
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from utils.logger import get_logger

logger = get_logger(__name__)


def check_health() -> Dict[str, Any]:
    """
    Perform comprehensive health checks on all system components.

    Checks performed:
        1. **API Keys**: Verifies GROQ_API_KEY is configured
        2. **Output Directory**: Verifies the output directory is writable
        3. **Agent Modules**: Verifies all 5 agent modules can be imported
        4. **Core Modules**: Verifies core pipeline modules load correctly

    Returns:
        dict: Health status report with the following structure::

            {
                "status": "healthy" | "degraded" | "unhealthy",
                "timestamp": "ISO 8601 timestamp",
                "version": "application version",
                "checks": {
                    "api_keys": {"status": "ok", "details": "..."},
                    "output_dir": {"status": "ok", "details": "..."},
                    "agents": {"status": "ok", "details": "..."},
                    "core": {"status": "ok", "details": "..."},
                }
            }
    """
    checks = {}
    overall_status = "healthy"

    # ── Check 1: API Keys ────────────────────────────────────────────
    try:
        if Config.GROQ_API_KEY:
            checks["api_keys"] = {"status": "ok", "details": "GROQ_API_KEY is configured"}
        else:
            checks["api_keys"] = {"status": "warning", "details": "GROQ_API_KEY not set"}
            overall_status = "degraded"
    except Exception as e:
        checks["api_keys"] = {"status": "error", "details": str(e)}
        overall_status = "unhealthy"

    # ── Check 2: Output Directory ────────────────────────────────────
    try:
        output_dir = Config.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        test_file = os.path.join(output_dir, ".health_check")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        checks["output_dir"] = {"status": "ok", "details": f"{output_dir} is writable"}
    except Exception as e:
        checks["output_dir"] = {"status": "error", "details": f"Output dir not writable: {e}"}
        overall_status = "unhealthy"

    # ── Check 3: Agent Modules ───────────────────────────────────────
    agent_modules = [
        "agents.planner.agent",
        "agents.research.agent",
        "agents.writer.agent",
        "agents.image.agent",
        "agents.builder.agent",
    ]
    agent_status = "ok"
    failed_agents = []
    for module_name in agent_modules:
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            agent_status = "error"
            failed_agents.append(f"{module_name}: {e}")

    if failed_agents:
        checks["agents"] = {
            "status": "error",
            "details": f"Failed to import: {', '.join(failed_agents)}"
        }
        overall_status = "unhealthy"
    else:
        checks["agents"] = {"status": "ok", "details": "All 5 agents importable"}

    # ── Check 4: Core Modules ────────────────────────────────────────
    try:
        importlib.import_module("core.state")
        importlib.import_module("core.graph")
        checks["core"] = {"status": "ok", "details": "Pipeline modules loaded"}
    except ImportError as e:
        checks["core"] = {"status": "error", "details": f"Core import failed: {e}"}
        overall_status = "unhealthy"

    return {
        "status": overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": Config.APP_VERSION,
        "checks": checks,
    }


# ── FastAPI Application ─────────────────────────────────────────────────

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(
        title="Agentic PPT Builder — Health",
        description="Health monitoring endpoint for the Agentic AI PPT Builder",
        version=Config.APP_VERSION,
    )

    @app.get("/health")
    async def health_endpoint():
        """
        Health check endpoint returning system status.

        Returns:
            JSON response with health status, checks, and metadata.
        """
        result = check_health()
        status_code = 200 if result["status"] == "healthy" else 503
        return JSONResponse(content=result, status_code=status_code)

    @app.get("/version")
    async def version_endpoint():
        """
        Version endpoint returning application info.

        Returns:
            JSON with version, configuration summary.
        """
        return {
            "version": Config.APP_VERSION,
            "config": Config.to_dict(),
        }

except ImportError:
    # FastAPI not installed — health check still works via check_health()
    app = None
    logger.warning("FastAPI not installed. Health endpoint not available as HTTP server.")


# ── Standalone Runner ────────────────────────────────────────────────────

if __name__ == "__main__":
    if app:
        import uvicorn
        print(f"🏥 Starting Health Check Server v{Config.APP_VERSION}")
        print(f"   → http://localhost:8080/health")
        print(f"   → http://localhost:8080/version")
        uvicorn.run(app, host="0.0.0.0", port=8080)
    else:
        # Fallback: just print health status
        import json
        result = check_health()
        print(json.dumps(result, indent=2))
