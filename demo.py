#!/usr/bin/env python3
"""
TMOS13 Demo CLI
Protocol-governed AI sessions. Deploy Yourself.
tmos13.ai
"""

import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

try:
    import anthropic
except ImportError:
    print("Run: pip install anthropic python-dotenv rich")
    exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import print as rprint
    RICH = True
except ImportError:
    RICH = False

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("Error: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
    exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
console = Console() if RICH else None

PACKS_DIR = Path(__file__).parent / "packs"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL = "claude-sonnet-4-20250514"
VERSION = "0.1.0-demo"


# ─── Pack Loader ─────────────────────────────────────────────────────────────

def load_packs():
    """Load all packs from the packs/ directory."""
    packs = {}
    for pack_dir in sorted(PACKS_DIR.iterdir()):
        if pack_dir.is_dir():
            manifest_path = pack_dir / "MANIFEST.md"
            if manifest_path.exists():
                content = manifest_path.read_text()
                packs[pack_dir.name] = {
                    "id": pack_dir.name,
                    "manifest": content,
                    "name": extract_field(content, "name") or pack_dir.name,
                    "description": extract_field(content, "description") or "",
                    "estimated_turns": extract_field(content, "estimated_turns") or "8-12",
                    "deliverable": extract_field(content, "deliverable") or "session_deliverable",
                }
    return packs


def extract_field(manifest: str, field: str) -> str:
    """Extract a field value from MANIFEST.md header block."""
    import re
    # Match **Field:** value or Field: value patterns
    patterns = [
        rf'\*\*{field.title()}\*\*:\s*(.+)',
        rf'\*\*{field}\*\*:\s*(.+)',
        rf'^{field}:\s*(.+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, manifest, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


# ─── Boot Screen ─────────────────────────────────────────────────────────────

def render_boot_screen(packs: dict):
    if RICH:
        console.print()
        console.print(
            Panel.fit(
                f"[bold white]13TMOS Console[/bold white] [dim]— demo runtime[/dim]",
                border_style="dim blue",
                padding=(0, 2),
            )
        )

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="dim", width=12)
        table.add_column(style="white")

        table.add_row("Version", VERSION)
        table.add_row("Model", MODEL)
        table.add_row("Packs", f"[bold red]{len(packs)} active[/bold red]")
        table.add_row("Vault", "./output/")
        table.add_row("Tagline", "[italic]Deploy Yourself.[/italic]")

        console.print(table)
        console.print()
    else:
        print("\n" + "─" * 52)
        print("  13TMOS Console — demo runtime")
        print("─" * 52)
        print(f"  Version  : {VERSION}")
        print(f"  Model    : {MODEL}")
        print(f"  Packs    : {len(packs)} active")
        print(f"  Vault    : ./output/")
        print("─" * 52)
        print()


def render_pack_list(packs: dict):
    if RICH:
        table = Table(show_header=True, box=None, padding=(0, 2))
        table.add_column("#", style="dim", width=4)
        table.add_column("Pack ID", style="cyan", width=22)
        table.add_column("Description", style="white")

        for i, (pack_id, pack) in enumerate(packs.items(), 1):
            table.add_row(str(i), pack_id, pack["description"][:60] + "..." if len(pack["description"]) > 60 else pack["description"])

        console.print(table)
        console.print()
    else:
        print("Available packs:\n")
        for i, (pack_id, pack) in enumerate(packs.items(), 1):
            print(f"  {i}. {pack_id:<24} {pack['description'][:50]}")
        print()


# ─── Session Runner ───────────────────────────────────────────────────────────

def build_system_prompt(pack: dict) -> str:
    """Build the system prompt from the pack manifest."""
    return f"""You are running a governed AI session under the TMOS13 protocol.

Pack: {pack['name']}
Deliverable: {pack['deliverable']}
Estimated turns: {pack['estimated_turns']}

Your governing protocol is below. Follow it precisely.

---

{pack['manifest']}

---

Session rules:
- Track turns. After each response, append: [turn N | fields: X/? | vault: pending]
- Ask one focused question per turn — do not overwhelm the user
- When all required fields are captured, produce the deliverable in a structured format
- The deliverable should be clearly delimited with :::deliverable and ::: markers
- Be concise and professional. This is not a chatbot. It is a governed workflow."""


def run_session(pack: dict):
    """Run a governed pack session."""
    pack_id = pack["id"]
    pack_name = pack["name"]
    session_id = f"{pack_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    messages = []
    turn = 0

    if RICH:
        console.print()
        console.print(Panel.fit(
            f"[bold white]{pack_name}[/bold white]",
            subtitle=f"[dim]session: {session_id}[/dim]",
            border_style="blue",
        ))
        console.print()
    else:
        print(f"\n{'─' * 52}")
        print(f"  Pack    : {pack_name}")
        print(f"  Session : {session_id}")
        print(f"{'─' * 52}\n")

    system_prompt = build_system_prompt(pack)
    deliverable_content = None

    while True:
        try:
            # Call the API
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=messages if messages else [{"role": "user", "content": "Begin the session."}],
            )

            assistant_message = response.content[0].text

            # Render assistant response
            if RICH:
                console.print(f"[dim cyan]●[/dim cyan] [white]{assistant_message}[/white]")
                console.print()
            else:
                print(f"\n{assistant_message}\n")

            # Check for deliverable
            if ":::deliverable" in assistant_message.lower() or "**deliverable**" in assistant_message.lower():
                deliverable_content = assistant_message
                save_deliverable(session_id, pack_id, deliverable_content)
                if RICH:
                    console.print(f"[bold green]✓ Deliverable saved to output/{session_id}.md[/bold green]")
                else:
                    print(f"\n✓ Deliverable saved to output/{session_id}.md")
                break

            messages.append({"role": "assistant", "content": assistant_message})

            # Get user input
            if RICH:
                user_input = console.input("[bold blue]You[/bold blue]  ")
            else:
                user_input = input("You  ").strip()

            if user_input.lower() in ("exit", "quit", "q"):
                print("\nSession ended.")
                break

            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})
            turn += 1

        except KeyboardInterrupt:
            print("\n\nSession interrupted.")
            break
        except anthropic.APIError as e:
            print(f"\nAPI error: {e}")
            break

    return session_id, deliverable_content


def save_deliverable(session_id: str, pack_id: str, content: str):
    """Write deliverable to output directory."""
    output_path = OUTPUT_DIR / f"{session_id}.md"
    timestamp = datetime.datetime.now().isoformat()

    full_content = f"""# TMOS13 Session Deliverable
**Pack:** {pack_id}
**Session:** {session_id}
**Timestamp:** {timestamp}
**Runtime:** 13TMOS Demo CLI v{VERSION}

---

{content}

---
*Generated by TMOS13 protocol-governed session · tmos13.ai*
"""
    output_path.write_text(full_content)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    packs = load_packs()

    if not packs:
        print("No packs found in packs/ directory.")
        exit(1)

    render_boot_screen(packs)
    render_pack_list(packs)

    # Pack selection
    while True:
        try:
            if RICH:
                choice = console.input("[dim]Enter pack name or number → [/dim]").strip()
            else:
                choice = input("Enter pack name or number → ").strip()

            if choice.isdigit():
                idx = int(choice) - 1
                pack_ids = list(packs.keys())
                if 0 <= idx < len(pack_ids):
                    selected = packs[pack_ids[idx]]
                    break
            elif choice in packs:
                selected = packs[choice]
                break
            else:
                print(f"Not found: '{choice}'. Try a pack name or number.")
        except KeyboardInterrupt:
            print("\nExiting.")
            exit(0)

    session_id, deliverable = run_session(selected)

    if RICH:
        console.print()
        console.print(f"[dim]Session complete. Output: [white]output/{session_id}.md[/white][/dim]")
        console.print()
    else:
        print(f"\nSession complete. Output: output/{session_id}.md\n")


if __name__ == "__main__":
    main()
