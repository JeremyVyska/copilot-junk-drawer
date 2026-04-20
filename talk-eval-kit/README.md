# 🎤 Talk Evaluation Kit

Transcribe your recorded conference talk and get a data-driven speaker coaching report — locally, privately, for free (aside from compute time).

Built around the principle that every speaker improves faster when they listen back with intent. This kit lets an agent do the heavy lifting so you can focus on the insights.

---

## 🎯 What this kit does

Given an audio recording of a talk (any length, any common format), this pipeline produces:

- **Full timestamped transcript** with word-level timestamps
- **Quantitative metrics**: speaking pace over time, filler word counts, pause detection, audience engagement markers
- **Rhetorical analysis**: signature phrase frequencies, metaphor density, improvisation vs. script
- **A 5-dimension coaching report** with specific timestamps, quotable moments, and ranked coaching priorities

Everything runs **locally**. No cloud uploads, no API costs, no privacy concerns.

---

## 🧾 The caveat (read this first)

**This kit produces its best output when you also provide:**
- The intended outline or deck of the talk
- Scripted moments you wanted to land (specific jokes, callbacks, thesis lines)
- Known improvisations or things that went off-plan
- Audience context (who were they, what were you promising them)

Without this context, the pipeline can still produce solid quantitative analysis (WPM, fillers, pauses) and generic rhetorical observations. But it cannot score your structural pacing against your intent, identify missed script moments, or distinguish "meaningful improvisation" from "rambling." The fidelity of analysis scales directly with the fidelity of context you provide.

**If you only have audio, you'll still get a useful report. If you have audio + outline + scripted moments, you'll get a coaching-grade report.**

---

## 📦 What's in the kit

```
talk-eval-kit/
├── README.md                    ← You are here
├── AGENT_INSTRUCTIONS.md        ← The persona/workflow doc for an agent
├── scripts/
│   ├── transcribe.py            ← faster-whisper wrapper, any audio → JSON
│   ├── analyze.py               ← Generic metrics (works on any talk)
│   ├── deep_pull.py             ← Config-driven passage extraction
│   ├── psych_analysis.py        ← Psychological-design dimension (Cialdini, peak-end, CTAs, etc.)
│   └── config.example.json      ← Example config to customize per talk
```

---

## 🚀 Quick start — manual

### 1. Install dependencies

```bash
pip install faster-whisper
```

For GPU acceleration (recommended for talks >30 min), also install CUDA toolkit. Not required — CPU works, just slower.

### 2. Convert your audio if needed

Most audio formats work directly (m4a, mp3, wav). If Whisper chokes on a weird format:

```bash
ffmpeg -i your-talk.m4a -ar 16000 -ac 1 your-talk.wav
```

That converts to mono 16kHz WAV, which Whisper loves.

### 3. Transcribe

```bash
python scripts/transcribe.py your-talk.wav
```

Takes 5-30 minutes depending on model size and hardware. Outputs `your-talk-transcript.json`.

For slower machines:
```bash
python scripts/transcribe.py your-talk.wav --model medium.en --device cpu
```

### 4. Run the quantitative analysis

```bash
python scripts/analyze.py your-talk-transcript.json
```

Prints a summary to console and saves `your-talk-metrics.json`.

### 5. Pull specific passages (optional but recommended)

Copy `scripts/config.example.json` and edit it for YOUR talk — update `landmarks`, `signature_phrases`, `thesis_phrases`, and `time_windows` to reflect your content.

```bash
cp scripts/config.example.json my-talk-config.json
# edit my-talk-config.json — change landmarks to your thesis phrases,
# signature_phrases to the words that should appear as refrains,
# thesis_phrases to the tighter subset that carries your core argument,
# time_windows to known moments you want pulled verbatim
```

Then run:

```bash
python scripts/deep_pull.py your-talk-transcript.json --config my-talk-config.json
```

### 6. Run the psychological-design analysis (Dimension 6)

This is the newer, deeper pass. It checks whether the talk deployed the evidence-based rhetorical moves that presentations research recommends: Cialdini's influence principles, peak-end rule, storytelling density, psychological safety framing, self-efficacy language, calls to action, and mere-exposure repetition of thesis phrases.

```bash
python scripts/psych_analysis.py your-talk-transcript.json --config my-talk-config.json
```

This one is opinionated. The detections are heuristic, not forensic — a "reciprocity marker detected" doesn't mean your reciprocity deployment was *effective*, just that the language was present. Use the output as a checklist, not a grade.

---

## 🤖 Agent-driven workflow (preferred)

The above works, but the REAL value is handing this to an AI coding agent and letting it orchestrate the full pipeline *with judgment*. The agent can:

- Ask you the right context questions upfront
- Help you build the config.json from your outline/deck
- Run the pipeline
- Interpret the metrics against your intent
- Produce the full 5-dimension synthesis report

### How to drive it

1. Open your agent (Claude Code, Cursor, etc.) in this kit directory
2. Feed it **the audio file, your outline/deck, and this kit's `AGENT_INSTRUCTIONS.md`**
3. Tell the agent: *"Follow AGENT_INSTRUCTIONS.md to evaluate this talk"*

The instructions doc handles the rest — it describes the persona, the workflow phases, what to ask you, what to produce, and style guidelines for the final report.

---

## 📊 What the metrics mean

**Overall WPM:**
- < 130 = slow, may feel plodding
- 130–150 = measured, conversational
- 150–170 = energetic conference range ✅
- 170–185 = brisk, confident
- > 185 = fast, risks losing audience

**Filler words per 10 min:**
- < 2 = excellent (rare speaker floor)
- 2–3 = normal
- 3–5 = worth watching
- \> 5 = coaching target (audible to listener)

**Pauses:**
- Dramatic pauses (>3s) are usually intentional — comic timing or impact landings
- Significant pauses (1.5–3s) include natural breath and slide transitions
- A LOW count of dramatic pauses may indicate the speaker is rushing through their best moments

**You:I ratio:**
- < 0.5 = monologue (self-focused)
- 0.5–0.9 = balanced
- \> 0.9 = audience-focused ✅

---

## 💡 Tips

- **Save your config per talk.** If you ever re-deliver, the landmarks are reusable.
- **Run this on your BEST talk too.** Knowing what works is as valuable as knowing what to fix.
- **Do a comparison over time.** Transcribe 3-4 talks from the past year, run the same analysis, see what's improving.
- **Don't over-correct on fillers.** Some "like" and "actually" are natural speech texture. The goal is awareness, not elimination.
- **The prosodic dimension is the one thing this kit CAN'T give you.** Tone, vocal energy, actual audience laughter volume — those require your ears. The kit should flag specific timestamps worth spot-listening to.

---

## 🏛️ Academic foundations

The kit isn't pure invention. The evaluation dimensions sit on top of decades of research on training evaluation, persuasion, and learning. Named explicitly so you know where to read more:

- **Kirkpatrick's Four Levels of Evaluation** (Reaction → Learning → Behavior → Results) — the standard framework for evaluating training impact. This kit handles **Level 1 (Reaction)** via vocal mechanics and audience-engagement proxies, plus some delivery-mechanics signals that correlate with Level 2 (Learning) outcomes. Levels 3 and 4 require follow-up surveys and business-outcome tracking that live outside a transcript — if you care about the full framework, pair this kit with a 30-day follow-up instrument.
- **Cialdini's Principles of Influence** — reciprocity, commitment/consistency, social proof, authority, liking, scarcity, unity. Scanned by `psych_analysis.py`.
- **Kahneman's peak-end rule and anchoring** — detected by the opening/closing analysis in `psych_analysis.py`.
- **Mayer's multimedia learning / dual coding** — the kit doesn't score visual design (it can't see your slides), but the storytelling density check nods at narrative transportation.
- **Bandura's self-efficacy** — detected via efficacy-framing language.
- **Edmondson's psychological safety** — detected via explicit invitation markers.
- **Knowles's adult learning theory, Deci & Ryan's self-determination** — not directly measurable from transcripts, but useful when reviewing the qualitative output.

A colleague — Steve Endow, fellow BC MVP and fellow presenter — compiled a full evidence-based synthesis of presentation evaluation frameworks that sharpened this kit significantly. If you want the theoretical depth, start with the primary sources above and work back.

The kit is *not* a substitute for reading the primary sources. It's a way to apply what's in them to your own recordings without needing a PhD in social psychology to run the numbers.

## 🛠️ What this kit won't do

- **It won't analyze vocal tone or energy** — Whisper gives us text, not melody. Agent should flag timestamps for you to spot-check.
- **It won't count audience laughter directly** — Whisper VAD filters non-speech. Use dramatic pauses after punchlines as a proxy.
- **It won't replace a live speech coach** — but it will tell you what to bring to one. Walk into coaching with data.

---

## 🏗️ Philosophy

This is a three-layer architecture in miniature:

- **Layer 1 (Binders):** The scripts + transcript = raw knowledge and tools
- **Layer 2 (Roles):** The agent instructions = a coaching persona
- **Layer 3 (Orchestration):** The workflow connecting them = systematic improvement

Apply agentic discipline to your own craft. That's the point.

---

## 🤝 Credits / origin

Built iteratively while evaluating a live conference talk delivery. The scripts were refined in real use, not theorized. Every bit of this pipeline was tested on a real 87-minute talk before being generalized.

If you improve it, PR welcome. If you evaluate 10 talks with it, share what you learned — the corpus of "what makes a talk land" is still being written, and every data point helps.

🎤 Good luck out there.
