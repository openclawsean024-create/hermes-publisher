"""Allow `python -m hermes_publisher` to work."""
from hermes_publisher.cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
