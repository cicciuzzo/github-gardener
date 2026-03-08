#!/usr/bin/env python3
"""
gardener.py — coltiva la griglia verde di GitHub con saggezza fuffaguru generata da Claude.
Leggi il README prima di giudicare.
"""

import os
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# --- Configurazione ---
SCRIPT_DIR    = Path(__file__).parent
DIARY_DIR     = SCRIPT_DIR / "diary"
README_FILE   = SCRIPT_DIR / "README.md"
ENV_FILE      = SCRIPT_DIR / ".env"
SKIP_PROB     = 0.30    # probabilità di saltare l'esecuzione
HOUR_START    = 8       # ora minima operativa
HOUR_END      = 23      # ora massima operativa
MODEL         = "claude-haiku-4-5-20251001"
README_MAX    = 100     # entry massime nel README prima di archiviare
ENTRY_SEP     = "<!-- entry -->"
REPO          = "cicciuzzo/github-gardener"

# Pesi delle attività: (tipo, peso)
ATTIVITA = [
    ("commit",  70),
    ("pr",      20),
    ("issue",   10),
]

PROMPT_FRASE = (
    "Scrivi una frase lunga esattamente come un tweet che scriverebbe un guru italiano "
    "della crescita personale: vaga, ispirazionale, piena di parole inglesi messe a caso, "
    "con emoji strategiche e almeno un concetto ovvio detto in modo complicato. "
    "Niente hashtag. Solo la frase, nient'altro."
)

PROMPT_ISSUE = (
    "Scrivi un titolo breve (max 60 caratteri) per una issue GitHub fittizia, "
    "nello stile di un guru della crescita personale italiana: vago, ispirazionale, "
    "con qualche parola inglese. Solo il titolo, nient'altro."
)


def load_env(path: Path) -> None:
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except FileNotFoundError:
        pass


def chiedi_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


# --- Logica README ---

def archivia_se_necessario(testo: str, now: datetime) -> str:
    parts  = testo.split(ENTRY_SEP)
    header = parts[0]
    entries = parts[1:]
    if len(entries) <= README_MAX:
        return testo
    da_archiviare = entries[:-README_MAX]
    da_tenere     = entries[-README_MAX:]
    DIARY_DIR.mkdir(exist_ok=True)
    archive = DIARY_DIR / f"{now.strftime('%Y')}.md"
    with open(archive, "a") as f:
        for e in da_archiviare:
            f.write(ENTRY_SEP + e)
    return header + ENTRY_SEP.join([""] + da_tenere)


def aggiorna_readme(frase: str, now: datetime) -> None:
    testo = README_FILE.read_text()
    entry = f"\n\n> {frase}\n\n*{now.strftime('%Y-%m-%d %H:%M')}*\n"
    testo = archivia_se_necessario(testo + ENTRY_SEP + entry, now)
    README_FILE.write_text(testo)


# --- Tipi di attività ---

def fai_commit(frase: str, now: datetime) -> None:
    """Commit diretto su main."""
    aggiorna_readme(frase, now)
    git(SCRIPT_DIR, "add", "-A")
    git(SCRIPT_DIR, "commit", "-m", f"🌱 wisdom drop - {now.strftime('%H:%M')}")
    git(SCRIPT_DIR, "push")


def fai_pr(frase: str, now: datetime) -> None:
    """Branch → commit → PR → merge → elimina branch."""
    branch = f"wisdom/{now.strftime('%Y-%m-%d-%H%M')}"

    git(SCRIPT_DIR, "checkout", "-b", branch)
    aggiorna_readme(frase, now)
    git(SCRIPT_DIR, "add", "-A")
    git(SCRIPT_DIR, "commit", "-m", f"✨ insight - {now.strftime('%H:%M')}")
    git(SCRIPT_DIR, "push", "-u", "origin", branch)

    # Apre e mergia la PR via gh
    pr_url = gh("pr", "create",
                "--repo", REPO,
                "--title", f"💡 Weekly insight {now.strftime('%Y-%m-%d')}",
                "--body", f"> {frase}",
                "--base", "main",
                "--head", branch)

    pr_number = pr_url.rstrip("/").split("/")[-1]
    gh("pr", "merge", pr_number, "--repo", REPO, "--merge", "--delete-branch")

    # Torna su main e aggiorna
    git(SCRIPT_DIR, "checkout", "main")
    git(SCRIPT_DIR, "pull")


def fai_issue(now: datetime) -> None:
    """Apre una issue fuffaguru e la chiude subito."""
    titolo = chiedi_claude(PROMPT_ISSUE)
    issue_url = gh("issue", "create",
                   "--repo", REPO,
                   "--title", titolo,
                   "--body", "Opened and resolved. The *journey* is the destination. 🚀")
    issue_number = issue_url.rstrip("/").split("/")[-1]
    gh("issue", "close", issue_number, "--repo", REPO)


# --- Main ---

def scegli_attivita() -> str:
    tipi   = [a[0] for a in ATTIVITA]
    pesi   = [a[1] for a in ATTIVITA]
    return random.choices(tipi, weights=pesi, k=1)[0]


def main() -> None:
    load_env(ENV_FILE)

    ora = datetime.now().hour
    if not (HOUR_START <= ora < HOUR_END):
        sys.exit(0)

    if random.random() < SKIP_PROB:
        sys.exit(0)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY non trovata", file=sys.stderr)
        sys.exit(1)

    try:
        now      = datetime.now()
        attivita = scegli_attivita()

        if attivita == "commit":
            frase = chiedi_claude(PROMPT_FRASE)
            fai_commit(frase, now)

        elif attivita == "pr":
            frase = chiedi_claude(PROMPT_FRASE)
            fai_pr(frase, now)

        elif attivita == "issue":
            fai_issue(now)

    except Exception as e:
        # Assicurati di tornare su main in caso di errore durante PR
        try:
            git(SCRIPT_DIR, "checkout", "main")
        except Exception:
            pass
        print(f"Errore [{attivita}]: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
