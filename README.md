# Restore Rapid Moves (F360 personal)
Python script for modifying G-code to restore rapid (G0/G1) moves after retracts.

Usage:
python3 restore.py input.nc output.nc retract_string

For example:
python3 restore.py input.ngc output.ngc "Z15. F#100"
