# Asciinema GIF Pipeline

Scripts for recording GEMC Python examples as terminal animations and converting them to GIFs,
optionally combined with a screen-capture video.

## Dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| `asciinema` | Record terminal sessions | `brew install asciinema` |
| `agg` | Convert `.cast` → `.gif` | `brew install agg` |
| `ffmpeg` | Convert `.mov` → `.gif`, resize, combine | `brew install ffmpeg` |
| `gifsicle` | Set infinite loop (no re-encode) | `brew install gifsicle` |

---

## Directory layout

```
scripts/asciinema/
├── record_example.sh     # Step 1 — record a GEMC example as a .cast file
├── cast_to_gif.sh        # Step 2a — convert .cast to .gif (terminal animation)
├── mov_to_gif.sh         # Step 2b — convert a .mov screen capture to .gif
├── combine_gifs.sh       # Step 3 — concatenate two GIFs into one
├── trim_gif.sh           # Step 3b — trim a GIF to a maximum duration
├── set_infinite_loop.sh  # Step 4 — make a GIF loop forever (in-place, no re-encode)
├── type_and_run.sh       # Internal — called by record_example.sh, not invoked directly
└── configs/
    └── simple_flux.env   # Per-example settings (recording + GIF knobs)
```

Output files (`.cast`, `.gif`) are written to the **repo root**.

---

## Step 1 — Record a terminal animation

```bash
./scripts/asciinema/record_example.sh simple_flux
# output: <repo_root>/simple_flux.cast
```

The script:
1. Finds `simple_flux.py` under `/opt/projects/gemc/src/examples/` automatically.
2. Starts `asciinema rec` with the terminal size from the config.
3. Types the source file character-by-character (via `type_and_run.sh`).
4. Runs `python3 simple_flux.py` so the recording ends with real output.

**To add a new example** just run with its name — no other setup needed:

```bash
./scripts/asciinema/record_example.sh box_volume
```

Optionally create `configs/box_volume.env` to tune the recording for that example.

### Recording knobs (`configs/<name>.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `COLS` | `100` | Terminal width in columns |
| `ROWS` | `30` | Terminal height in rows |
| `CHAR_DELAY` | `0.04` | Seconds per character (lower = faster typing) |
| `LINE_PAUSE` | `0.15` | Pause after each line |
| `BLANK_PAUSE` | `0.5` | Pause on blank lines |

---

## Step 2a — Convert `.cast` to `.gif`

Requires `agg` (`brew install agg`).

```bash
./scripts/asciinema/cast_to_gif.sh simple_flux
# output: <repo_root>/simple_flux.gif

# Override speed on the command line (config value used otherwise)
./scripts/asciinema/cast_to_gif.sh simple_flux 2.5
```

### GIF knobs (`configs/<name>.env` or env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `GIF_SPEED` | `1.0` | Playback speed multiplier (2.0 = twice as fast) |
| `GIF_FPS` | `20` | Frames-per-second cap |
| `GIF_FONT_SIZE` | `14` | Font size in pixels |

The CLI `speed` argument overrides `GIF_SPEED` from the config file.

---

## Step 2b — Convert a `.mov` screen capture to `.gif`

Requires `ffmpeg` (`brew install ffmpeg`).

```bash
./scripts/asciinema/mov_to_gif.sh /path/to/demo.mov screen_demo
# output: <repo_root>/screen_demo.gif

# Resize to 900px wide while converting
./scripts/asciinema/mov_to_gif.sh /path/to/demo.mov screen_demo 900
```

Arguments:

| Position | Required | Description |
|----------|----------|-------------|
| 1 | yes | Path to the `.mov` file (any ffmpeg-readable format works) |
| 2 | no | Output basename (default: input filename without extension) |
| 3 | no | Resize width in pixels — height auto-scales |

Uses two-pass palette generation for high colour quality.

### Knobs (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `GIF_FPS` | `20` | Frames per second |
| `GIF_WIDTH` | _(original)_ | Resize width; CLI arg 3 takes precedence |

---

## Step 3 — Combine two GIFs

Requires `ffmpeg` (`brew install ffmpeg`).
Plays the first GIF, then the second, in a single looping GIF.

```bash
./scripts/asciinema/combine_gifs.sh simple_flux.gif screen_demo.gif simple_flux_full
# output: <repo_root>/simple_flux_full.gif

# Resize both to 900px wide before combining
./scripts/asciinema/combine_gifs.sh simple_flux.gif screen_demo.gif simple_flux_full 900
```

Arguments:

| Position | Required | Description |
|----------|----------|-------------|
| 1 | yes | First GIF (path or filename relative to repo root) |
| 2 | yes | Second GIF (path or filename relative to repo root) |
| 3 | no | Output basename (default: `combined`) |
| 4 | no | Resize width — both GIFs scaled to this width |

If no width is given, the second GIF is resized to match the first GIF's natural width.

Because two GIFs scaled to the same width can still have different heights (different aspect
ratios), both are automatically letterboxed to the taller of the two scaled heights before
concatenation. Black bars are added symmetrically on the shorter one.

Uses two-pass palette generation on the full concatenated stream for consistent colour quality.

### Knobs (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `GIF_FPS` | `20` | Output frames per second |
| `GIF_WIDTH` | _(gif1 width)_ | Resize width; CLI arg 4 takes precedence |

---

## Step 3b — Append a PNG still to the end of a GIF

Requires `ffmpeg` and `gifsicle` (both already listed in dependencies).

The PNG clip must be padded to the same height as the GIF so it is vertically centred.
Probe the GIF height first, then pass it to the `pad` filter.

```bash
# Get the GIF height
H=$(ffprobe -v error -probesize 5000000 -analyzeduration 0 \
    -select_streams v:0 -show_entries stream=height \
    -of default=noprint_wrappers=1:nokey=1 input.gif)

# Convert PNG: scale to target width, pad to GIF height, centre vertically
# -t 4 = hold for 4 seconds (adjust as needed)
ffmpeg -y -nostdin -loop 1 -i image.png -t 4 \
    -vf "fps=2,scale=1200:-1:flags=lanczos,pad=1200:${H}:(ow-iw)/2:(oh-ih)/2" \
    /tmp/png_clip.gif

# Concatenate
gifsicle input.gif /tmp/png_clip.gif > output.gif
```

`fps=2` is enough for a static image (2 frames per second × duration = total frames).

---

## Step 3b — Trim a GIF to a maximum duration

Requires `ffmpeg` (`brew install ffmpeg`).

```bash
# Trim to first 10 seconds, save as new file
./scripts/asciinema/trim_gif.sh simple_flux_full 10 simple_flux_trimmed

# Trim in-place (overwrite original)
./scripts/asciinema/trim_gif.sh simple_flux_full 10
```

Arguments:

| Position | Required | Description |
|----------|----------|-------------|
| 1 | yes | Input GIF (bare name, `.gif`, or absolute path) |
| 2 | yes | Maximum duration in seconds |
| 3 | no | Output basename — omit to overwrite input |

---

## Step 4 — Set infinite loop

Requires `gifsicle` (`brew install gifsicle`).

Rewrites the GIF loop metadata — no re-encoding, no quality loss.

```bash
./scripts/asciinema/set_infinite_loop.sh simple_flux_full
```

Accepts a bare name, a name with `.gif` extension, or an absolute path:

```bash
./scripts/asciinema/set_infinite_loop.sh simple_flux_full
./scripts/asciinema/set_infinite_loop.sh simple_flux_full.gif
./scripts/asciinema/set_infinite_loop.sh /path/to/any.gif
```

---

## Full workflow example

```bash
cd /opt/projects/gemc/home

# 1. Record the terminal animation
./scripts/asciinema/record_example.sh simple_flux

# 2a. Convert to GIF (speed set in configs/simple_flux.env)
./scripts/asciinema/cast_to_gif.sh simple_flux

# 2b. Convert a screen-capture video to GIF at matching width
./scripts/asciinema/mov_to_gif.sh ~/Desktop/pyvista_demo.mov pyvista_demo 900

# 3. Combine: terminal GIF first, then the screen-capture GIF
./scripts/asciinema/combine_gifs.sh simple_flux.gif pyvista_demo.gif simple_flux_full 900

# 3b. (Optional) Append a PNG still at the end — e.g. a logo or summary slide
H=$(ffprobe -v error -probesize 5000000 -analyzeduration 0 -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 gemc_full.gif)
ffmpeg -y -nostdin -loop 1 -i logo.png -t 4 -vf "fps=2,scale=900:-1:flags=lanczos,pad=900:${H}:(ow-iw)/2:(oh-ih)/2" /tmp/png_clip.gif
gifsicle simple_flux_full.gif /tmp/png_clip.gif > simple_flux_final.gif

# 3c. (Optional) Trim to a maximum duration
./scripts/asciinema/trim_gif.sh simple_flux_final 12

# 4. Set infinite loop (no re-encode)
./scripts/asciinema/set_infinite_loop.sh simple_flux_final
```

Final file: `<repo_root>/simple_flux_final.gif`

---

## Per-example config file format

Create `configs/<example_name>.env` to store all settings for an example in one place.
All variables are optional — omit any you want to leave at the default.

```bash
# configs/simple_flux.env

# Recording
COLS=100
ROWS=30
CHAR_DELAY=0.00001
LINE_PAUSE=0.001
BLANK_PAUSE=0.0001

# GIF conversion (cast_to_gif.sh)
GIF_SPEED=4.0
GIF_FPS=40
GIF_FONT_SIZE=14
```
