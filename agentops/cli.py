import argparse
import json
from .http_client import HttpClient
from os import environ


def fetch_ttd_cache(ttd_id):
    endpoint = environ.get("AGENTOPS_API_ENDPOINT", "https://api.agentops.ai")  # TODO
    payload = json.dumps({"ttd_id": ttd_id}).encode("utf-8")
    ttd_res = HttpClient.post(f"{endpoint}/v2/get_ttd", payload)
    # if ttd_res.status_code != 200:
    #     print(f"Failed to fetch TTD with status code {ttd_res.status_code}")
    #     return

    print(f"Successfully fetched TTD cache for TTD ID {ttd_id}")
    prompt_to_returns_map = {
        (
            str({"messages": item["prompt"]["messages"]})
            if item["prompt"].get("type") == "chatml"
            else str(item["prompt"])
        ): item["returns"]
        for item in ttd_res.body  # TODO: rename returns to completion_override
    }
    with open("ttd.json", "w") as file:
        json.dump(prompt_to_returns_map, file)


def main():
    parser = argparse.ArgumentParser(description="AgentOps CLI")
    parser.add_argument(
        "-ttd",
        type=str,
        help="Given a TTD ID, fetches the cache file for Time Travel Debugging",
    )

    args = parser.parse_args()

    if args.ttd:
        fetch_ttd_cache(args.ttd)


if __name__ == "__main__":
    main()
