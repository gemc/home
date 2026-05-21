## GIF Demo Pipeline

Scripts in `scripts/asciinema/` record GEMC Python examples as terminal animations,
optionally combine them with a screen-capture video, and produce a final looping GIF.

Full documentation: [`scripts/asciinema/README.md`](scripts/asciinema/README.md)

**Install dependencies:**

```bash
brew install asciinema agg ffmpeg gifsicle
```

**Typical workflow:**

```bash
# 1. Record terminal typing + run of a GEMC example → .cast
./scripts/asciinema/record_example.sh simple_flux

# 2a. Convert .cast → .gif  (speed/fps/font set in configs/simple_flux.env)
./scripts/asciinema/cast_to_gif.sh simple_flux

# 2b. Convert a .mov screen capture → .gif
./scripts/asciinema/mov_to_gif.sh ~/Desktop/demo.mov screen_demo 1200

# 3. Concatenate both GIFs (auto-letterboxes to match heights)
./scripts/asciinema/combine_gifs.sh simple_flux.gif screen_demo.gif combined 1200

# 3b. (Optional) Append a PNG still at the end (vertically centred)
H=$(ffprobe -v error -probesize 5000000 -analyzeduration 0 -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 combined.gif)
ffmpeg -y -nostdin -loop 1 -i logo.png -t 4 -vf "fps=2,scale=1200:-1:flags=lanczos,pad=1200:${H}:(ow-iw)/2:(oh-ih)/2" /tmp/png_clip.gif
gifsicle combined.gif /tmp/png_clip.gif > final.gif

# 3c. (Optional) Trim to a maximum duration in seconds
./scripts/asciinema/trim_gif.sh final 12

# 4. Set infinite loop (no re-encode)
./scripts/asciinema/set_infinite_loop.sh final
```

Per-example recording and GIF knobs live in `scripts/asciinema/configs/<name>.env`.

---

#### Link checker:

https://validator.w3.org/checklink/

https://www.deadlinkchecker.com/



# Tabs in markdown.

- the plugin read_file is installed in _plugins
- the file tabs.html is in _includes

This will produce tabs, however not if gh-pages is used.

```
{% capture tab1 %}
  {{ "_documentation/databases/fields.md" | read_file }}
{% endcapture %}

{% capture tab2 %}
  {{ "_documentation/databases/fields.md" | read_file }}
{% endcapture %}

{% include tabs.html 
   id="example-tabs-2"
   count=2
   tab1_title="First tab"
   tab1_content=tab1
   tab2_title="Second tab"
   tab2_content=tab2
%}

```

### Run Periodically:

(put all these in a single script please)

```
./scripts/periodic.sh
```


---

- [ICONS](https://feathericons.com)

---

## Gist:

https://gist.github.com


