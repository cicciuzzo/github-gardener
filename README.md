# github-gardener

**Progetto artistico di vibecoding realizzato con [Claude Code](https://claude.ai/claude-code).**

Sì, la griglia verde è finta. No, non me ne vergogno.

Un Raspberry Pi 3 si sveglia a orari irregolari, chiede a Claude Haiku di generare una perla di saggezza da fuffaguru della crescita personale italiana, e la committa qui. A volte apre PR. A volte apre issue e le chiude subito. Il pattern è semirandom per sembrare plausibilmente umano.

Tutto il codice — dal bot alla configurazione systemd — è stato scritto in vibecoding con Claude Code. Il bot genera le frasi con Claude Haiku. Turtles all the way down.

Il codice è pubblico. Il trucco è dichiarato. Se stai leggendo questo README, congratulazioni: sei più attento del 99% dei recruiter.

> **Nota per recruiter:** se sei arrivato fin qui, hai già dimostrato più attenzione della media. I miei progetti veri sono negli altri repo. Questo è solo il giardiniere.

## Come funziona

- **Timer systemd** su RPi3 lancia `gardener.py` ogni ~ora (±20min random)
- **Pattern da lavoratore full-time**: quasi mai durante orario ufficio (9–18), più attivo la sera e nel weekend
- **Giorni a zero commit** capitano — come nella vita vera
- **Attivo solo 08:00–23:00** (anche i fuffaguru dormono)
- Claude Haiku genera la frase, lo script sceglie cosa fare:

| Azione | Probabilità | Cosa succede |
|---|---|---|
| Commit diretto | 70% | Frase aggiunta a questo README, push su main |
| Pull Request | 20% | Branch, commit, PR, merge, cleanup |
| Issue | 10% | Titolo fuffaguru, aperta e chiusa immediatamente |

- Le frasi si accumulano qui sotto — dopo 100 entry le più vecchie finiscono in `diary/`

## Setup

```bash
git clone https://github.com/cicciuzzo/github-gardener && cd github-gardener
cp .env.example .env   # inserisci ANTHROPIC_API_KEY
sudo cp gardener.service gardener.timer /etc/systemd/system/
sudo systemctl enable --now gardener.timer
```

---

## 🔮 Il muro della saggezza
<!-- entry -->

> La vera essenza del mindset vincente risiede nella capacità di implementare daily habits che generino un momentum positivo attraverso l'ottimizzazione costante del tuo inner game, perché il successo non è una destinazione ma un lifestyle 🚀✨💪

*2026-03-08 19:09*
<!-- entry -->

> La vera essenza del mindset vincente risiede nella capacità di implementare una strategia olistica di self-improvement attraverso la consapevolezza emotiva, perché solo quando allinei il tuo purpose con l'energia dell'universo puoi raggiungere il next level della tua existence 🚀✨💎

*2026-03-09 15:59*
<!-- entry -->

> La vera essenza del tuo personal growth risiede nella capacità di implementare una mindset shift radicale, trasformando le tue limiting beliefs in unlocked potential attraverso la consapevolezza conscia del momento presente 🚀✨🔥

*2026-03-09 16:02*
