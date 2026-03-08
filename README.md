# github-gardener 🌱

Un bot onesto che coltiva la griglia verde della mia attività GitHub.

## Cosa fa

Gira su un Raspberry Pi 3, si sveglia a orari irregolari durante la giornata,
chiede a Claude Haiku di scrivere un haiku in italiano, lo salva in un diario
mensile e fa commit + push. La griglia diventa più verde. Tutti sanno come
funziona perché è scritto qui.

Non è una truffa — è un progetto con un obiettivo dichiarato e un'implementazione
visibile. Il codice fa esattamente quello che dice il README.

## Esempio di output

```
### 2026-03-08 14:32

vento tra i rami
il gatto guarda lontano
pioggia sul vetro
```

## Come funziona

- `gardener.py` viene lanciato da un systemd timer ogni ora circa
- Ha una probabilità del 30% di saltare l'esecuzione (pattern irregolare)
- Opera solo tra le 08:00 e le 23:00
- Genera un haiku via Claude Haiku API su tema random
- Appende il haiku a `diary/YYYY-MM.md` con timestamp
- Fa `git commit` e `git push`

## Setup

```bash
git clone https://github.com/cicciuzzo/github-gardener
cd github-gardener
cp .env.example .env
# inserisci la tua ANTHROPIC_API_KEY nel .env
```

Installa il systemd service (vedi `gardener.service`) e abilitalo:

```bash
sudo cp gardener.service /etc/systemd/system/
sudo systemctl enable --now gardener.timer
```
<!-- entry -->

> La vera essenza del mindset vincente risiede nella capacità di implementare daily habits che generino un momentum positivo attraverso l'ottimizzazione costante del tuo inner game, perché il successo non è una destinazione ma un lifestyle 🚀✨💪

*2026-03-08 19:09*
