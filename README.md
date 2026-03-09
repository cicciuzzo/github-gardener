# 🌱 github-gardener

**Due fuffaguru, un Raspberry Pi, e una griglia verde su GitHub.**

Questo repo è un progetto artistico di *vibecoding*: un Raspberry Pi 3 si sveglia a intervalli irregolari e genera una conversazione fittizia tra due guru italiani della crescita personale — **Maikol Pirozzi** (mindset imprenditoriale, anglicismi corporate) e **Big Duca** (wellness olistico, vibrazioni alte).

## Come funziona

- Un **timer systemd** lancia `gardener.py` ogni ~1h (±20 min di jitter)
- Un **modello probabilistico** (distribuzione Beta, correlazione di sessione, moltiplicatore giornaliero) decide se eseguire o saltare — simulando il pattern di attività di uno sviluppatore reale
- Se esegue, sceglie un'attività: **commit** (60%), **pull request** (15%), **code review** (15%), **issue** (10%)
- Ogni commit aggiunge una nuova battuta alla chat qui sotto, generata da Claude Haiku con il contesto delle ultime 10 risposte
- Minimo garantito: 2 interazioni al giorno grazie a un meccanismo di catch-up serale

## Stack

`Python 3` · `Claude Haiku` · `GitHub CLI` · `systemd` · `Raspberry Pi 3`

Sì, la griglia verde è finta. No, non me ne vergogno. 💚

---

## 💬 La chat dei guru
<!-- entry -->

> La vera essenza del tuo personal growth risiede nella capacità di implementare una mindset shift radicale, trasformando le tue limiting beliefs in unlocked potential attraverso la consapevolezza conscia del momento presente 🚀✨🔥

*2026-03-09 16:02*
<!-- entry -->

> **Maikol Pirozzi**: Esatto bro, ma qui il vero game changer è il data-driven approach: trackare le tue abitudini, misurare i KPI del tuo mindset, scalare quello che funziona e pivotare rapidamente 📊💯 Solo così il tuo personal brand diventa davvero disruptive 🚀

*2026-03-09 16:41*
<!-- entry -->

> **Big Duca**: Sì sì, ma Maikol ascolta... i numeri sono importanti però la vera vibrazione arriva quando entri in deep flow con il tuo inner purpose, senza forzare il match tra ego e intuizione 🧘‍♂️💫 L'energia non ha KPI, fratello

*2026-03-09 17:00*
