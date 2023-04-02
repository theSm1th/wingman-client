import serial
import requests
import json
import time

ser = serial.Serial("COM9", 9600, timeout=0.05)


def lead_spacing(value, desired_length, to_replace):
    value = str(value)
    if len(value) != desired_length:
        to_add = desired_length - len(value)
        return to_add * to_replace + value
    else:
        return value


def post_spacing(value, desired_length, to_replace):
    value = str(value)
    if len(value) != desired_length:
        to_add = desired_length - len(value)
        return value + (to_add * to_replace)
    else:
        return value


def comp_get_stats():
    data_get = requests.get("http://localhost:8085/data.json")
    json_data = json.loads(data_get.content)

    cpu_data = json_data["Children"][0]["Children"][1]["Children"]
    cpu_temp = int(cpu_data[3]["Children"][0]["Value"][:-5])
    cpu_util = int(cpu_data[4]["Children"][0]["Value"][:-4])

    gpu_data = json_data["Children"][0]["Children"][3]["Children"]
    gpu_temp = int(gpu_data[3]["Children"][0]["Value"][:-5])
    gpu_util = int(gpu_data[4]["Children"][0]["Value"][:-4])

    fan_data = json_data["Children"][0]["Children"][0]["Children"][0]["Children"][2]["Children"]
    avg_fan_spd = int((int(fan_data[0]["Value"][:-4]) +
                       int(fan_data[1]["Value"][:-4]) +
                       int(fan_data[2]["Value"][:-4])) / 3)
    print(gpu_data[3]["Children"][0]["Value"])

    return {"cpu_temp": cpu_temp, "cpu_util": cpu_util,
            "gpu_temp": gpu_temp, "gpu_util": gpu_util,
            "avg_fan_spd": avg_fan_spd}


def check_league_stats():
    try:
        active_player = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False)
    except requests.exceptions.ConnectionError:
        return False
    print(active_player.status_code)
    if active_player.status_code == 200:
        active_player_data = json.loads(active_player.content)
        summoner_name, champion_name = active_player_data["summonerName"], active_player_data["abilities"]["E"]["id"][
                                                                           :-1]

        player_scores = requests.get(f"https://127.0.0.1:2999/liveclientdata/playerscores?summonerName={summoner_name}",
                                     verify=False)
        player_scores_data = json.loads(player_scores.content)
        kills, deaths, assists, cs = player_scores_data["kills"], player_scores_data["deaths"], player_scores_data[
            "assists"], player_scores_data["creepScore"]

        return [champion_name, kills, deaths, assists, cs]
    else:
        return False


if __name__ == "__main__":
    while True:
        data = comp_get_stats()
        league_data = check_league_stats()
        if league_data is not False:
            header = post_spacing("{} {}CS {}/{}/{}".format(league_data[0],
                                                            league_data[4],
                                                            league_data[1],
                                                            league_data[2],
                                                            league_data[3]), 20, " ")
        else:
            header = "WINGMAN             "
        sp_util_fan = "{}%  {} RPM  {}%".format(lead_spacing(data["cpu_util"], 3, " "),
                                                lead_spacing(data["avg_fan_spd"], 4, " "),
                                                lead_spacing(data["gpu_util"], 3, " "))

        sp_temps = "{}C CPU    GPU {}C".format(lead_spacing(data["cpu_temp"], 3, " "),
                                               lead_spacing(data["gpu_temp"], 3, " "))
        flavour_text = "Blast Processing..."
        string_to_write = f"{header}{sp_util_fan}{sp_temps}{flavour_text}"
        ser.write(string_to_write.encode())
        time.sleep(2.5)