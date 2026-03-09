#!/usr/bin/env python3
"""
gardener.py — coltiva la griglia verde di GitHub con saggezza fuffaguru generata da Claude.
Leggi il README prima di giudicare.
"""

import json
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
STATE_FILE    = SCRIPT_DIR / ".state.json"
HOUR_START    = 8       # ora minima operativa
HOUR_END      = 24      # esteso a mezzanotte (22-24 leggermente attivo)
MODEL         = "claude-haiku-4-5-20251001"


# ---------------------------------------------------------------------------
# Distribuzione probabilistica — validata da Roberto Battiti (Caltech)
#
# Migliorie rispetto alla v1:
# - Moltiplicatore giornaliero Beta(a,b) → giorni caldi/freddi
# - Skip interi weekend con P=0.25
# - Sessioni correlate: un commit passato aumenta P dei successivi
# - Pausa pranzo 12-13 leggermente attiva
# - Tarda sera 22-24 leggermente attiva
# ---------------------------------------------------------------------------

# Prob di SKIP base per fascia oraria (prima del moltiplicatore giornaliero)
DAILY_MIN_EXEC = 2   # minimo garantito di esecuzioni al giorno
_SKIP_BASE = {
    # (weekend, hour_range) → skip_prob
    # Lun-Ven
    (False,  8):  0.70,   # mattina presto
    (False,  9):  0.80,   # lavoro
    (False, 10):  0.80,
    (False, 11):  0.80,
    (False, 12):  0.75,   # pausa pranzo — commit veloce
    (False, 13):  0.80,
    (False, 14):  0.80,
    (False, 15):  0.80,
    (False, 16):  0.80,
    (False, 17):  0.80,
    (False, 18):  0.65,   # uscita dal lavoro
    (False, 19):  0.35,   # sera: fascia più attiva
    (False, 20):  0.35,
    (False, 21):  0.40,
    (False, 22):  0.60,   # tarda sera
    (False, 23):  0.70,
    # Sab-Dom
    (True,   8):  0.85,
    (True,   9):  0.75,
    (True,  10):  0.60,
    (True,  11):  0.55,
    (True,  12):  0.60,
    (True,  13):  0.70,
    (True,  14):  0.70,
    (True,  15):  0.55,
    (True,  16):  0.50,
    (True,  17):  0.55,
    (True,  18):  0.60,
    (True,  19):  0.65,
    (True,  20):  0.65,
    (True,  21):  0.70,
    (True,  22):  0.70,
    (True,  23):  0.80,
}


def _load_state() -> dict:
    """Carica stato persistente (moltiplicatore giornaliero, sessione)."""
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state: dict) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def _beta_sample(a: float, b: float) -> float:
    """Campione da Beta(a,b) usando metodo di Jöhnk — zero dipendenze."""
    while True:
        u1 = random.random()
        u2 = random.random()
        x = u1 ** (1.0 / a)
        y = u2 ** (1.0 / b)
        if x + y <= 1.0:
            return x / (x + y)


def _get_day_multiplier(state: dict, now: datetime) -> float:
    """
    Moltiplicatore giornaliero: scala le probabilità di esecuzione.
    Campionato una volta per giorno e salvato nello state.
    Beta(2,5) per feriali → media 0.28, produce giorni caldi e freddi
    Beta(1.5,3) per weekend → media 0.33, più varianza
    """
    today_str = now.strftime("%Y-%m-%d")
    if state.get("day_date") == today_str:
        return state["day_mult"]

    weekend = now.weekday() >= 5

    # Skip intero weekend con P=0.25
    if weekend and random.random() < 0.25:
        mult = 0.0  # giornata completamente vuota
    else:
        mult = _beta_sample(1.5, 3.0) if weekend else _beta_sample(2.0, 5.0)
        # Normalizza: mult ∈ [0, 1], moltiplica la P(exec)
        # Scaliamo per avere media ~1.0: dividiamo per la media della Beta
        mean = 1.5 / 4.5 if weekend else 2.0 / 7.0
        mult = mult / mean  # ora media ≈ 1.0, range [0, ~3]
        mult = min(mult, 2.5)  # cap per evitare giornate esplosive

    state["day_date"] = today_str
    state["day_mult"] = mult
    return mult


def _get_session_boost(state: dict, now: datetime) -> float:
    """
    Sessioni correlate: se l'ultimo commit è stato < 90 min fa,
    aumenta la probabilità di eseguire (simula burst).
    Ritorna un fattore moltiplicativo per P(exec): 1.0 = nessun boost, >1 = boost.
    """
    last_exec_ts = state.get("last_exec_ts", 0)
    elapsed_min  = (now.timestamp() - last_exec_ts) / 60.0

    if elapsed_min < 30:
        return 2.5   # appena committato → alta prob di continuare
    elif elapsed_min < 60:
        return 1.8
    elif elapsed_min < 90:
        return 1.3
    return 1.0


def _get_day_exec_count(state: dict, now: datetime) -> int:
    """Numero di esecuzioni oggi."""
    today_str = now.strftime("%Y-%m-%d")
    if state.get("day_date") != today_str:
        return 0
    return state.get("day_exec_count", 0)


def _should_force_catchup(state: dict, now: datetime) -> bool:
    """
    Catch-up serale: se non abbiamo raggiunto il minimo giornaliero,
    forza l'esecuzione nelle ultime ore. Sovrascrive anche day_mult=0.
    """
    count = _get_day_exec_count(state, now)
    if count >= DAILY_MIN_EXEC:
        return False
    if now.hour >= 22 and count == 0:
        return True                        # 0 commit alle 22+: forza
    if now.hour >= 21 and count <= 1:
        return random.random() < 0.85      # 85% di forzare
    return False


def should_skip(now: datetime) -> bool:
    """Decisione finale: skip o eseguire, con tutti i fattori."""
    state = _load_state()

    day_mult = _get_day_multiplier(state, now)
    _save_state(state)

    # Catch-up: sovrascrive tutto, incluso day_mult=0
    if _should_force_catchup(state, now):
        return False

    if day_mult == 0.0:
        return True  # giornata off

    weekend   = now.weekday() >= 5
    base_skip = _SKIP_BASE.get((weekend, now.hour), 0.80)
    base_exec = 1.0 - base_skip

    session_boost = _get_session_boost(state, now)

    # P(exec) finale = base × day_mult × session_boost, clampato a [0, 0.8]
    p_exec = min(base_exec * day_mult * session_boost, 0.80)

    return random.random() > p_exec


def record_execution(now: datetime) -> None:
    """Registra che un'esecuzione è avvenuta (per sessioni correlate e conteggio giornaliero)."""
    state = _load_state()
    state["last_exec_ts"] = now.timestamp()
    today_str = now.strftime("%Y-%m-%d")
    if state.get("day_date") == today_str:
        state["day_exec_count"] = state.get("day_exec_count", 0) + 1
    else:
        state["day_exec_count"] = 1
    _save_state(state)

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

    # Sincronizza con il remote (può fallire se offline)
    try:
        git(SCRIPT_DIR, "pull", "--rebase")
    except Exception:
        pass

    now = datetime.now()
    if not (HOUR_START <= now.hour < HOUR_END):
        sys.exit(0)

    if should_skip(now):
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

        record_execution(now)

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
