#!/usr/bin/env bash

# execute these manually

 # rm -f a.cast ; asciinema rec a.cast
 # pyvista ; clear ; PROMPT='%F{green} $%f ' ; ./simple.sh

# --- Function to simulate typing a command line by line ---
type_command() {
    local cmd="$1"
    # Use the shell's current prompt marker or a custom one for effect
    PS1_MARKER=">>> "
    echo -n "$PS1_MARKER"

    # Print the command char by char with a small delay
    # This delay is what asciinema records as "typing"
    for (( i=0; i<${#cmd}; i++ )); do
        echo -n "${cmd:$i:1}"
        sleep 0.0 # Adjust this speed (0.03s is pretty quick)
    done
    echo "" # Newline after typing
}

# 1. Define the actual Python code as a single block (using a "here document")
# Note: The backslash-n (\n) characters are *not* needed when using cat << 'EOF'
PYTHON_CODE=$(cat << 'EOF'
from gconfiguration import autogeometry
from gvolume import GVolume

cfg = autogeometry(
    "examples",
    "simple_flux",
    auto_show=False,
    enable_pyvista=True,
    use_background_plotter=True,
)

world_size = 110
gvolume = GVolume("root")
gvolume.description = "World"
gvolume.make_box(world_size * 0.5, world_size * 0.5, world_size * 0.5)
gvolume.material = "G4_AIR"
gvolume.color = "ghostwhite"
gvolume.style = 0
gvolume.publish(cfg)

target_dz = 20
target_radius = 5
gvolume = GVolume("Target")
gvolume.mother = "root"
gvolume.description = "Simple Carbon Target"
gvolume.make_tube(0, target_radius, target_dz, 0, 360)
gvolume.material = "G4_C"
gvolume.color = "metallic, darkgreen"
gvolume.publish(cfg)

flux_z = 50
flux_dx = 1
flux_dim = world_size * 0.8
gvolume = GVolume("FluxPlane")
gvolume.mother = "root"
gvolume.description = "Flux Scoring Plane"
gvolume.make_box(flux_dim * 0.5, flux_dim * 0.5, flux_dx * 0.5)
gvolume.material = "G4_AIR"
gvolume.color = "FAFAD2"
gvolume.set_position(0, 0, flux_z)
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
gvolume.publish(cfg)
cfg.show()
EOF
)

# --- Execution for Asciinema Recording ---

echo "Starting interactive geometry definition..."

# 2. Loop through the Python code, "typing" each line for the recording
while IFS= read -r line; do
    # Check if the line has *any* content other than the newline character (i.e., not a completely blank line)
    # The 'type_command' function adds the '>>> ' prompt.

    if [[ -n "$line" ]]; then
        # For lines with content, "type" them out
        trimmed_line=$(echo "$line" | sed 's/^[ \t]*//;s/[ \t]*$//')
        type_command "$trimmed_line"
        sleep 0.1 # Pause after typing a command
    else
        # For empty lines, just print the prompt and a newline (simulating hitting Enter)
        echo ">>> "
        sleep 0.3 # A longer pause for dramatic effect (the "thinking" pause)
    fi

done <<< "$PYTHON_CODE"


python3 -c "${PYTHON_CODE}"


sleep 2