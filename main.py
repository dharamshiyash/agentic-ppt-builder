"""
CLI Entrypoint — main.py
-------------------------
Run the Agentic AI PPT Builder from the command line.

Usage:
    python main.py --topic "Artificial Intelligence in Healthcare"
    python main.py --topic "Climate Change" --slides 8 --font Arial --depth Detailed
"""
import argparse
import os
import sys

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.config import Config
from orchestrator.agent_controller import run_pipeline

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="🤖 Agentic AI PowerPoint Builder — CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Artificial Intelligence in Healthcare"
  python main.py --topic "Climate Change" --slides 8 --font Arial --depth Detailed
        """
    )
    parser.add_argument(
        "--topic", "-t",
        type=str,
        required=True,
        help="The presentation topic (required)."
    )
    parser.add_argument(
        "--slides", "-s",
        type=int,
        default=Config.DEFAULT_SLIDE_COUNT,
        help=f"Number of slides to generate (default: {Config.DEFAULT_SLIDE_COUNT})."
    )
    parser.add_argument(
        "--font", "-f",
        type=str,
        default="Calibri",
        choices=["Arial", "Calibri", "Times New Roman", "Consolas"],
        help="Font to use throughout the presentation (default: Calibri)."
    )
    parser.add_argument(
        "--depth", "-d",
        type=str,
        default="Concise",
        choices=["Minimal", "Concise", "Detailed"],
        help="Content depth per slide (default: Concise)."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"\n🤖 Agentic AI PowerPoint Builder")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Topic  : {args.topic}")
    print(f"  Slides : {args.slides}")
    print(f"  Font   : {args.font}")
    print(f"  Depth  : {args.depth}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # Validate API keys
    if not Config.GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY is not set. Please add it to your .env file.")
        sys.exit(1)

    print("🔄 Starting multi-agent pipeline...")
    print("  [1/5] PlannerAgent    → planning slide outline...")
    print("  [2/5] ResearchAgent   → searching the web for facts...")
    print("  [3/5] WriterAgent     → writing slide content...")
    print("  [4/5] ImageAgent      → sourcing images...")
    print("  [5/5] BuilderAgent    → assembling the .pptx file...")
    print()

    try:
        final_state = run_pipeline(
            topic=args.topic,
            slide_count=args.slides,
            font=args.font,
            depth=args.depth,
        )

        ppt_path = final_state.get("final_ppt_path", "")
        if ppt_path:
            print(f"✅ Presentation generated successfully!")
            print(f"📄 Saved to: {os.path.abspath(ppt_path)}\n")
        else:
            print("❌ Pipeline completed but no PPT file was generated. Check logs for details.\n")
            sys.exit(1)

    except ValueError as ve:
        print(f"❌ Input Error: {ve}\n")
        sys.exit(1)
    except Exception as exc:
        logger.error(f"CLI pipeline error: {exc}", exc_info=True)
        print(f"❌ Unexpected error: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
