import argparse
from .time_travel import fetch_time_travel_id, set_time_travel_active_state


def main():
    parser = argparse.ArgumentParser(description="AgentOps CLI")
    parser.add_argument(
        "-ttid",
        type=str,
        help="Given a Time Travel ID, fetches the cache file for Time Travel Debugging. Turns on feature by default",
    )
    parser.add_argument(
        "-tt",
        type=str,
        help="Turns on or off Time Travel Debugging",
        choices=["on", "off"],
    )

    args = parser.parse_args()

    if args.ttid:
        fetch_time_travel_id(args.ttid)

    if args.tt:
        set_time_travel_active_state(args.tt)


if __name__ == "__main__":
    main()
