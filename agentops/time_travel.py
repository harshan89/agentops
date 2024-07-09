import json
from .http_client import HttpClient
from os import environ
from .log_config import logger
from .helpers import singleton


@singleton
class TimeTravel:
    def __init__(self):
        self._time_travel_configured_correctly = True
        self._time_travel_map = None


def output_ttd_state_to_terminal(message=None):
    if TimeTravel()._time_travel_configured_correctly:
        # print("\033[43m", end="")  # Set background color to yellow # TODO in logger
        logger.warning(f"Activating Time Travel Debugging")
    else:
        print("\033[0m", end="")  # Reset to default colors
        if message:
            logger.warning(f"Deactivating Time Travel Debugging: {message}")
        else:
            logger.warning(f"Deactivating Time Travel Debugging")


def fetch_time_travel_id(ttd_id):
    try:
        with open("time_travel.config", "w") as config_file:
            config_file.write("Time_Travel_Debugging_Active=True\n")

        endpoint = environ.get("AGENTOPS_API_ENDPOINT", "https://api.agentops.ai")
        payload = json.dumps({"ttd_id": ttd_id}).encode("utf-8")
        ttd_res = HttpClient.post(f"{endpoint}/v2/get_ttd", payload)
        if ttd_res.code != 200:
            raise Exception(
                f"Failed to fetch TTD with status code {ttd_res.status_code}"
            )

        logger.info(f"Successfully fetched TTD cache for TTD ID {ttd_id}")
        prompt_to_returns_map = {
            (
                str({"messages": item["prompt"]["messages"]})
                if item["prompt"].get("type") == "chatml"
                else str(item["prompt"])
            ): item["returns"]
            for item in ttd_res.body  # TODO: rename returns to completion_override
        }
        with open("time_travel.json", "w") as file:
            json.dump(prompt_to_returns_map, file)
    except Exception as e:
        _time_travel_configured_correctly = False
        output_ttd_state_to_terminal(e)


def fetch_response_from_time_travel_cache(kwargs):
    TimeTravel()
    if not check_time_travel_active():
        return

    if TimeTravel()._time_travel_map is None:
        try:
            with open("time_travel.json", "r") as file:  # TODO: name
                TimeTravel()._time_travel_map = json.load(file)
        except FileNotFoundError:
            return

    if TimeTravel()._time_travel_map:
        search_prompt = str({"messages": kwargs["messages"]})
        result_from_cache = TimeTravel()._time_travel_map.get(search_prompt)
        if result_from_cache:
            logger.info(f"Time Travel Hit for prompt: %s", search_prompt)
            return result_from_cache
        else:
            logger.info(f"Time Travel Miss for prompt: %s", search_prompt)
    else:
        _time_travel_configured_correctly = False
        output_ttd_state_to_terminal()


def check_time_travel_active():
    try:
        with open("time_travel.config", "r") as config_file:
            for line in config_file:
                key, value = line.strip().split("=")
                if key == "Time_Travel_Debugging_Active" and value == "True":
                    output_ttd_state_to_terminal()
                    return True
    except Exception as e:
        pass
    return False


def set_time_travel_active_state(active_setting):
    with open("time_travel.config", "a") as config_file:
        if active_setting == "on":
            config_file.write("Time_Travel_Debugging_Active=True\n")
        else:
            config_file.write("Time_Travel_Debugging_Active=False\n")
