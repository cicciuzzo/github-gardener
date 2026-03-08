# Regole progetto

## Sicurezza credenziali — TASSATIVO

- NON leggere MAI il contenuto di `.env`, `~/.git-credentials`, o qualsiasi file che possa contenere chiavi API, token o credenziali
- NON eseguire MAI comandi che stampino il contenuto di questi file (cat, echo, print, grep su questi file, ecc.)
- NON loggare MAI variabili d'ambiente che contengano chiavi (ANTHROPIC_API_KEY, token GitHub, ecc.)
- In caso di dubbio, chiedere all'utente prima di toccare qualsiasi file di configurazione sensibile

## Agenti globali disponibili

- **`security-auditor`**: audit di sicurezza per librerie esterne prima dell'import
- **`dependencies-minimizer`**: analizza codice e suggerisce come ridurre dipendenze esterne
