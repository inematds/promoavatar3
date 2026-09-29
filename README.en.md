# promoavatar3

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Three videos per audience instead of one. The bot writes the scripts and STOPS;
`/aprovar C#N` releases the avatar, download, and reel.

**This project is AUTONOMOUS** (since 2026-08-06). It has already been described as "the same
as promoavatar": that is no longer true. The reel engine (`scripts/`), the layouts
(`templates/`), and the editing skill live HERE. Changes to the targets, prompts, or
templates there **do not affect anything here**.

`promoavatar` was frozen from 2026-08-06 to 2026-08-09 and **has resumed evolving**.
This does not merge the two: they remain separate systems, each with its own engine and
targets. The difference in purpose is the same as always—there, it is **one** video per
audience; here, it's **three** (reach, authority, promotional).

## 📖 User guide

Complete guide (landing page + walkthrough): **https://inematds.github.io/promoavatar3/guia/en/**

Reference: `C#7`. `promoavatar` uses `A#`, and `promoclub` uses `P#`—the bot rejects
references with the wrong prefix.

Usage, options, and the table of the three types: `HELP.md` (or `/promoavatar3 help` in
chat). Engineering decisions and the reasoning behind each one: `CLAUDE.md`.

## What belongs in this repo and what belongs in the bot

This split applies on both sides and avoids duplicated documentation that falls out of
sync:

| here (domain) | in [`inemaccbot`](https://github.com/inematds/inemaccbot) (engine) |
|---|---|
| **who** the audience is (`alvos` in `flow.json`), each audience's trigger and closing | how a queue works, lease, resumption, gate |
| **which channel** it goes to (`lives2`, `lives22`…) — by NAME, never the path | where that name lives on disk |
| the text phase **prompt** (`prompts/`) | how a phase prompt is executed |
| the reel **template** (`templates/`) and engine (`scripts/`) | how the `reel.montar` phase launches the engine |
| `TEMPLATE-AVATAR` and the voice engine (`engine`, `voice_id`) | the `\| api`, `\| creditos`, and `\| estudio` routes and which wallet each draws from → [`docs/rotas-de-avatar.md`](https://github.com/inematds/inemaccbot/blob/master/docs/rotas-de-avatar.md) |
| the CTA (`cta/cta-9x16.mp4`) | installation, `.env`, systemd, chat commands |

Short rule: **if it changes with the audience, it belongs here; if it changes with the machine, it belongs there.**

## Where to change what

| I want to change | File |
|---|---|
| audience, trigger, closing, channel | `flow.json` → `alvos` |
| **add** a new audience | `docs/adicionar-publico.md` (5 files, no restart) |
| how the text is written (the 3 versions, the `## IMAGENS` sections) | `prompts/fase1-3versoes.md` |
| avatar, voice, engine, studio template | `flow.json` → `avatar_id`, `voice_id`, `engine`, `template` |
| the reel layout | `templates/` (and `template` at the root of `flow.json`) |
| the reel engine | `scripts/montar-reel.py` and neighboring files |
| the help text the chat responds with | `HELP.md` |
| the CTA video | `cta/cta-9x16.mp4` (version-controlled since 2026-08-08) |

**Nothing here has a machine-specific path.** What used to depend on (`localhost:8000` for
inemaimg, the Groq key) became environment variables with the same defaults as before—
`INEMAIMG_HOST`, `INEMAIMG_MODEL`, `GROQ_ENV_PATH`, documented in the bot's
`.env.example`. The regression check is for `git grep /home/ -- .` to return zero in
version-controlled files.

## Images: GPU here, API elsewhere

`scripts/gen-imagem.py` talks to more than one provider. **The default has not changed**—
anyone running it at home still uses the local GPU without configuring anything:

| `IMG_PROVEDOR` | generator | cost | seed |
|---|---|---|---|
| `inemaimg` *(default)* | local GPU, `flux2-klein` | zero | **respected** |
| `agnes` | Agnes AI API, `agnes-image-2.1-flash` | **US$ 0**, ~10 s/image | **not available** |
| `kie`, `fal` | — | — | **not implemented**: the script refuses instead of pretending |

On the VPS: `IMG_PROVEDOR=agnes` and the key in `IMG_ENV_PATH` (a file with
`AGNES_API_KEY=`, `chmod 600`) — or `AGNES_API_KEY` directly in the environment.

**Two things change when moving off the GPU, and neither can be fixed here:**

1. **Determinism is lost.** Agnes does not accept a seed, so the same `--seed-key`
   generates a different image each time it renders. Only inemaimg fulfills “same reel,
   same image”—including over a tunnel (`ssh -R 8000:localhost:8000 <vps>`), which is the
   option to consider if reproducibility matters more than independence.
2. **The requested size becomes a suggestion.** Measured: we requested 1088x736 and got
   1248x832. The adapter **normalizes** by center-cropping (never stretching, which would
   distort faces)—without this, `preparar.py` would regenerate the entire image every time,
   because it compares dimensions to decide whether to reuse it.

Provider details, including what was measured for each:
[`inemaimg/docs/prompt-por-provedor.md`](https://github.com/inematds/inemaimg/blob/main/docs/prompt-por-provedor.md).

## The three types, and why they are not three variations

| suffix | type | duration | what the audience does next |
|---|---|---|---|
| `-alc` | reach | 25–40s | shares, comments |
| `-aut` | authority | 35–60s | saves, follows |
| `-pro` | promotional | 30–45s | clicks |

It is not the same script with three hooks. These are three different FUNCTIONS, and what
separates them is the closing: `-alc` has no commercial CTA at all (spoken or in the
reel), `-aut` lightly features the brand, and `-pro` converts. A video that tries to be
all three at once is a promotional video with a friendly opening—and it gets the least
reach of the three.

Recommended publishing order: reach → authority → promotional.

## The text prompt (`prompts/fase1-3versoes.md`)

In this order: the targets and what each suffix means · FIXED CONTEXT (Nei and Tiza as
managers) · DO NOT TOUCH THE MACHINE · STEP ZERO (central thesis, reason to watch,
demonstrable element) · **topic for debate** · the 14 writing rules · what changes for
each type · the output contract.

Variables injected by the bot: `{{input}}` (the topic), `{{publicos}}` (the REAL targets
in the flow, already filtered by `| alvos=`), `{{pasta}}` (where to save,
absolute), `{{ref}}`, `{{saida}}`.

### Debate topic: the prompt takes a position

A topic that arrives as an open question ("is this good or bad?", "what do you think?")
had a predictable result: the agent explained both sides and closed with "the important
thing is to be prepared." Correct but lukewarm—no one comments on fence-sitting.

The cause was not a lack of talent: rules 9 and 10 (do not invent data, do not invent
urgency) make the agent retreat to the middle ground, the only place where it is sure it
is not asserting anything.

This cost more here than in `promoavatar`: **without a position on the table, the three
types collapse into one.** They all become the same balanced summary in three wrappers,
and `-alc` becomes impossible—“opposing opinion,” the format that gets the most
engagement on a controversial topic, does not exist unless someone takes a side.

So the prompt tells the agent to take a side and **write down in `resumo-estrategico.md`
which position it took and why**. With the position defined, the three really do diverge:
`-alc` argues for it, `-aut` explains the mechanics that support it, and `-pro` turns it
into a practical consequence. This does not loosen rules 9 and 10: opinions are allowed;
invented facts are not.

**The position you give takes precedence over the agent's.** If you write your own
position in the topic, it uses yours; the block is only there for when you have not
written one. Writing your own is still the best approach—along with a concrete fact (so
the PROOF line is not empty) and the question you want in the comments.

Since the summary states the chosen position, you can disagree with it **at the gate**,
before generating any avatars. Here that means three manual renders per audience, not one.

## Captions: the reel's are ours; the studio's are inherited

Since 2026-08-13, **the reel adds captions by default** (word by word, amber on the
keyword—`docs/legenda.md`), using the same engine as promoavatar. The studio captions are
something else, and come from outside:

The `baixar` phase prefers `video_url_caption` (the MP4 with **burned-in** captions) when
HeyGen returns it filled in, and falls back to the clean `video_url` when it does not
(`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`). If it was recorded with captions
in the studio, the reel includes them; if it was recorded without them, it does not—the bot
does not choose.

Two consequences that no code can undo: burned-in captions are framed for 16:9 and may be
cropped or collide with the bottom bar in a 9:16 reel; and they stack with the REEL
captions, which have been **enabled by default** here since 2026-08-13 (the engine started
adding captions, just like promoavatar—see `docs/legenda.md`). Recorded with captions in
the studio and left reel captions enabled? You get **two** sets. Choosing one means
turning off the other, and studio captions are turned off in `TEMPLATE-AVATAR`, not here.
In this repo, that means three videos per audience, not one.

## What runs without a model

Of the four phases, **only the text phase uses an LLM**. The other three are functions:

| phase | how it runs |
|---|---|
| text | agent—writes the 3 scripts per audience |
| avatar (`\| estudio`) | **Playwright script** in the HeyGen studio (~50s/audience) |
| download | function—finds by TITLE and downloads |
| reel | **function**—`scripts/montar-reel.py`, then delivers to the channel |

Measured in promoavatar before the port: the cost per video dropped from **US$ 3,09 to
US$ 0,18** when the avatar and reel stopped being handled by an agent. The breakdown is
in `inemaccbot/docs/custo-por-fase-a19-a29.md`.

## The reel engine lives here

`scripts/montar-reel.py` chains: prepare → gate 1 (lint + pacing) → render →
reviewer → CTA → QC. Fixed names (`motion/corpo.mp4`, `final/reel.mp4`,
`qc/mosaico.png`), exit 3 when a gate fails.

**The entry gate is the text's `## IMAGENS` section** (rule 11b of the phase 1 prompt):
one line per spoken SEGMENT, with `headline:` and `hook:`. Without it, `preparar.py`
exits with code 3 and the reel is not assembled—it is not a style preference; it is what
prevents the reel from coming out with an empty panel or an invented headline.

The layouts are in `templates/`, and the default is the `template` at the root of
`flow.json`; a target can specify its own.

## Note: everything here is frozen when created

`flow.json` and the prompt are copied into the flow when it is created. Editing them here
only affects NEW flows—a flow in progress does not change its rules midway. To apply
changes to an existing one, create another.
