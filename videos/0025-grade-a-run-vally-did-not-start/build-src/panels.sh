#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Line numbers that depend on the run are
# computed, so the work is in panels.py; this wrapper keeps the same command as the other lessons.
set -e
python3 "$(dirname "$0")/panels.py"
