# promoavatar3

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Tres videos por público, en lugar de uno. El bot escribe los textos y SE DETIENE;
`/aprovar C#N` habilita avatar, descarga y reel.

**Este proyecto es AUTÓNOMO** (desde 2026-08-06). Antes se describía como «igual
que promoavatar»: ya no lo es. El motor del reel (`scripts/`), los diseños
(`templates/`) y la skill de edición viven AQUÍ. Cambiar los objetivos, prompts o
templates de allí **no afecta nada aquí**.

`promoavatar` estuvo congelado de 2026-08-06 a 2026-08-09 y **volvió a evolucionar**.
Eso no une los dos proyectos: siguen siendo sistemas separados, cada uno con su motor y sus
objetivos. La diferencia de propósito sigue siendo la de siempre: allí hay **un** video por público; aquí
son **tres** (alcance, autoridad, promocional).

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/promoavatar3/guia/es/**

Referencia: `C#7`. `promoavatar` usa `A#`; `promoclub`, `P#`: el bot rechaza
las referencias con el prefijo equivocado.

Uso, opciones y la tabla de los tres tipos: `HELP.md` (o `/promoavatar3 help` en el
chat). Las decisiones de ingeniería y el motivo de cada una: `CLAUDE.md`.

## Qué pertenece a este repo y qué pertenece al bot

La división se aplica a ambos lados y evita duplicar documentación que luego queda
desactualizada de forma inconsistente:

| aquí (dominio) | en [`inemaccbot`](https://github.com/inematds/inemaccbot) (motor) |
|---|---|
| **quién** es el público (`alvos` en `flow.json`), el disparador y el cierre de cada uno | cómo funciona una cola, lease, reanudación, portón |
| **a qué canal** va (`lives2`, `lives22`…) — por el NOMBRE, nunca la ruta | dónde se encuentra ese nombre en el disco |
| el **prompt** de la fase de texto (`prompts/`) | cómo se ejecuta un prompt de fase |
| el **template** del reel (`templates/`) y el motor (`scripts/`) | cómo la fase `reel.montar` activa el motor |
| `TEMPLATE-AVATAR` y el motor de voz (`engine`, `voice_id`) | las rutas `\| api`, `\| creditos`, `\| estudio` y de qué bolsillo sale cada una → [`docs/rotas-de-avatar.md`](https://github.com/inematds/inemaccbot/blob/master/docs/rotas-de-avatar.md) |
| el CTA (`cta/cta-9x16.mp4`) | instalación, `.env`, systemd, comandos del chat |

Regla breve: **si cambia según el público, va aquí; si cambia según la máquina, va allí.**

## Dónde cambiar cada cosa

| quiero cambiar | archivo |
|---|---|
| público, disparador, cierre, canal | `flow.json` → `alvos` |
| **agregar** un público nuevo | `docs/adicionar-publico.md` (5 archivos, sin reinicio) |
| cómo se escribe el texto (las 3 versiones, los `## IMAGENS`) | `prompts/fase1-3versoes.md` |
| avatar, voz, motor, template del estudio | `flow.json` → `avatar_id`, `voice_id`, `engine`, `template` |
| el diseño del reel | `templates/` (y `template` en la raíz de `flow.json`) |
| el motor del reel | `scripts/montar-reel.py` y archivos relacionados |
| la ayuda que responde el chat | `HELP.md` |
| el video de CTA | `cta/cta-9x16.mp4` (con control de versiones desde 2026-08-08) |

**Nada aquí tiene rutas de máquina.** Lo que dependía de ellas (`localhost:8000` de
inemaimg, la clave de Groq) pasó a ser variables de entorno con el mismo valor
predeterminado de antes: `INEMAIMG_HOST`, `INEMAIMG_MODEL`, `GROQ_ENV_PATH`, documentadas en el
`.env.example` del bot. La prueba que detecta regresiones es que
`git grep /home/ -- .` dé cero resultados en archivos versionados.

## Las imágenes: GPU aquí, API afuera

`scripts/gen-imagem.py` se comunica con más de un proveedor. **El valor predeterminado no cambió**:
quien lo ejecuta en casa sigue usando la GPU local, sin configurar nada:

| `IMG_PROVEDOR` | quién genera | costo | seed |
|---|---|---|---|
| `inemaimg` *(default)* | la GPU local, `flux2-klein` | cero | **respetada** |
| `agnes` | API de Agnes AI, `agnes-image-2.1-flash` | **US$ 0**, ~10 s/imagen | **no existe** |
| `kie`, `fal` | — | — | **no implementados**: el script los rechaza en vez de simular que funcionan |

En la VPS: `IMG_PROVEDOR=agnes` y la clave en `IMG_ENV_PATH` (archivo con
`AGNES_API_KEY=`, `chmod 600`) — o `AGNES_API_KEY` directamente en el entorno.

**Al salir de la GPU cambian dos cosas, y ninguna tiene solución aquí:**

1. **El determinismo disminuye.** Agnes no acepta seed, así que la misma `--seed-key`
   genera una imagen diferente en cada render. Solo inemaimg cumple con «mismo reel, misma
   imagen», incluso a través de un túnel (`ssh -R 8000:localhost:8000 <vps>`), opción a
   considerar si la reproducibilidad importa más que la independencia.
2. **El tamaño solicitado pasa a ser una sugerencia.** Medido: pedimos 1088x736 y volvió
   1248x832. El adaptador **normaliza** recortando por el centro (nunca estira,
   porque deformaría el rostro); sin esto, `preparar.py` volvería a generar la imagen cada vez,
   porque compara las dimensiones para decidir si la reutiliza.

Detalle por proveedor, con lo medido en cada uno:
[`inemaimg/docs/prompt-por-provedor.md`](https://github.com/inematds/inemaimg/blob/main/docs/prompt-por-provedor.md).

## Los tres tipos y por qué no son tres variaciones

| sufijo | tipo | duración | qué hace el público después |
|---|---|---|---|
| `-alc` | alcance | 25–40s | comparte, comenta |
| `-aut` | autoridad | 35–60s | guarda, sigue |
| `-pro` | promocional | 30–45s | hace clic |

No es el mismo guion con tres ganchos. Son tres FUNCIONES diferentes, y lo que las
distingue es el cierre: `-alc` no tiene ningún CTA comercial (ni hablado ni en el
reel), `-aut` menciona la marca de pasada, `-pro` convierte. Un video que intenta ser
los tres al mismo tiempo es promocional con una apertura simpática, y es el de menor
alcance de los tres.

Orden de publicación recomendado: alcance → autoridad → promocional.

## El prompt del texto (`prompts/fase1-3versoes.md`)

En este orden: los objetivos y el significado de cada sufijo · CONTEXTO FIJO (Nei y Tiza
como gestores) · NO TOQUES LA MÁQUINA · PASO CERO (tesis central, motivo para
verlo, elemento demostrable) · **tema que es debate** · las 14 reglas de
escritura · qué cambia en cada tipo · el contrato de salida.

Variables que inyecta el bot: `{{input}}` (el tema), `{{publicos}}` (los objetivos
REALES del flujo, ya filtrados por `| alvos=`), `{{pasta}}` (dónde guardar,
ruta absoluta), `{{ref}}`, `{{saida}}`.

### Tema que es DEBATE: el prompt fija una postura

Un tema planteado como pregunta abierta («¿esto es bueno o malo?», «¿qué opinas?»)
tenía un resultado predecible: el agente explicaba ambos lados y
terminaba con «lo importante es prepararse». Correcto y tibio: nadie comenta con
un equilibrista.

La causa no era falta de talento: son las reglas 9 y 10 (no inventar datos, no
inventar urgencia) las que hacen que el agente retroceda al punto medio, el único lugar
donde tiene certeza de no estar afirmando nada.

Aquí eso costaba más que en `promoavatar`: **sin una postura definida, los
tres tipos se reducen a uno solo.** Los tres se convierten en el mismo resumen equilibrado
con tres envoltorios, y `-alc` se vuelve imposible: «opinión contraria», el formato que más
interacción genera en un tema polémico, no existe sin alguien que tome partido.

Por eso el prompt indica que se tome partido y **se escriba en `resumo-estrategico.md` qué
postura se fijó y por qué**. Con la postura definida, los tres se diferencian
de verdad: `-alc` la defiende, `-aut` explica el mecanismo que la sustenta, `-pro`
la convierte en una consecuencia práctica. Esto no relaja las reglas 9 y 10: se permite
opinar; inventar hechos, no.

**La postura que indiques prevalece sobre la suya.** Si escribes la tuya sobre el tema, la
usará; el bloque solo existe para cuando no hayas escrito ninguna. Sigue siendo mejor
escribir la tuya, junto con un hecho concreto (para que la línea PROVA no quede vacía) y
la pregunta que quieres que te respondan en los comentarios.

Como el resumen indica la postura elegida, puedes disentir de ella **en el portón**, antes de
generar cualquier avatar. Aquí esto significa tres renders manuales por público, no uno.

## Subtítulos: los del reel son nuestros; los del estudio vienen de afuera

Desde 2026-08-13 **el reel lleva subtítulos por defecto** (palabra por palabra, ámbar en la
palabra clave; `docs/legenda.md`), con el mismo motor de promoavatar. Los del
estudio son otra cosa y vienen de afuera:

La fase `baixar` prefiere `video_url_caption` (el MP4 con los subtítulos **incrustados**)
cuando HeyGen lo devuelve con contenido, y recurre a `video_url` limpio cuando no
(`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`). Si el video se grabó con subtítulos en el
estudio, el reel los tendrá; si se grabó sin ellos, saldrá sin ellos: el bot no elige.

Hay dos consecuencias que ningún código puede deshacer: los subtítulos incrustados vienen
encuadrados para 16:9 y en el reel 9:16 pueden quedar cortados o chocar con la base; y se suman a
los subtítulos del REEL, que desde 2026-08-13 están **activados por defecto** aquí (el motor
empezó a generarlos, igual que promoavatar; consulta `docs/legenda.md`). Si el video se grabó con
subtítulos en el estudio y dejaste activados los del reel, aparecen **dos**. Para elegir uno,
hay que desactivar el otro, y los del estudio se desactivan en `TEMPLATE-AVATAR`, no aquí.
En este repo eso aplica a tres videos por público, no uno.

## Qué funciona sin modelo

De las cuatro fases, **solo la de texto usa un LLM**. Las otras tres son funciones:

| fase | cómo funciona |
|---|---|
| texto | agente: escribe los 3 guiones por público |
| avatar (`\| estudio`) | **script** de Playwright en el estudio de HeyGen (~50s/público) |
| descargar | función: busca por TÍTULO y descarga |
| reel | **función**: `scripts/montar-reel.py` y lo entrega en el canal |

Medido en promoavatar antes de la migración: el costo por video bajó de **US$ 3,09 a
US$ 0,18** cuando el avatar y el reel dejaron de ser tarea del agente. El detalle está en
`inemaccbot/docs/custo-por-fase-a19-a29.md`.

## El motor del reel vive aquí

`scripts/montar-reel.py` encadena: preparar → portón 1 (lint + ritmo) → render →
revisor → CTA → QC. Nombres fijos (`motion/corpo.mp4`, `final/reel.mp4`,
`qc/mosaico.png`), exit 3 cuando falla un portón.

**El portón de entrada es la sección `## IMAGENS` del texto** (regla 11b del prompt de la
fase 1): una línea por SEGMENTO del discurso, con `headline:` y `hook:`. Sin ella,
`preparar.py` termina con exit 3 y el reel no se monta; no es una preferencia de
estilo, es lo que evita que el reel salga con un panel vacío o un titular inventado.

Los diseños están en `templates/` y el predeterminado es el `template` de la raíz de
`flow.json`; un objetivo puede fijar el suyo.

## Atención: todo esto se congela al crear el flujo

`flow.json` y el prompt se copian dentro del flujo en el momento en que nace. Editar aquí solo
afecta a flujos NUEVOS: las reglas de un flujo en curso no cambian a mitad de camino. Para que se
aplique a lo que ya existe, crea otro.
