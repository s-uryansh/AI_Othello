from __future__ import annotations
import os
import runpy
import sys

def main():
    """
    Run the scripts/analyze_validation_results.py script to generate validation plots.
    This uses runpy on the script file to avoid import/package issues.
    """
    # locate the analyze script relative to this file:
    script_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "analyze_validation_results.py")
    )
    if not os.path.exists(script_path):
        print(f"Error: analyze script not found at {script_path}", file=sys.stderr)
        sys.exit(2)

    try:
        # run the script as __main__ (so its if __name__ == "__main__": block executes)
        runpy.run_path(script_path, run_name="__main__")
    except Exception as e:
        print(f"Error running analyze script: {e}", file=sys.stderr)
        sys.exit(1)
    print("Plot generation completed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
