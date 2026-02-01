# Score Capture

Capture, Detect, Stitch and Reclip music score/TAB
from scroll video to generate printable images.

## i18n support TODO

## Run/Build from source

Download source and enter project root dir

    git clone https://github.com/Carrot-shreds/score_capture.git
    cd score_capture

Install uv environment (Optional)

    pip install uv 
    (or)
    curl -LsSf https://astral.sh/uv/install.sh | sh

Install packages (no dev dependencies by default)

     uv sync
     (or)
     uv sync --dev

Run main entry

    uv run main.py
    (Linux) bash main.sh

Get update

    git pull

Build exe

    uv run ./build.py
