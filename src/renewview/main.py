"""RenewView — Main entry point."""

import sys
from datetime import datetime

from dotenv import load_dotenv

from renewview.flow import RenewViewFlow


def main():
    """Run the full RenewView pipeline."""
    load_dotenv()
    print(f"\n  RenewView starting at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Python {sys.version.split()[0]}")

    flow = RenewViewFlow()
    result = flow.kickoff()
    print(f"\n  Flow finished. State: {flow.state.stage}")
    return result


def plot_flow():
    """Save flow diagram as PNG."""
    RenewViewFlow().plot("renewview_flow")
    print("Saved renewview_flow.png")


if __name__ == "__main__":
    main()
