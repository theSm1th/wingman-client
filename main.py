import serial
import requests
import json


# ser = serial.Serial("COM9", 9600, timeout=0.05)
# ser.write(b"WINGMAN             00.0* CPU  GPU 00.0*100%  1000 RPM  100%####################")

def format_temp(to_format):
    if to_format >= 100:
        return "OVERL"
    return "{:.1f}*".format(to_format)


def remove_percent_space(dataIn):
    dataIn = dataIn.replace("%", "").replace(" ", "")
    print(dataIn)
    return int(dataIn)


def comp_get_stats():
    # data_get = requests.get("http://localhost:8085/data.json")
    # json_data = json.loads(data_get.content)
    with open("data.json", "r") as file:
        json_data = json.loads(file.readlines()[0])

    cpu_data = json_data["Children"][0]["Children"][1]["Children"]
    cpu_temp = cpu_data[3]["Children"][0]["Value"]
    cpu_util = cpu_data[4]["Children"][0]["Value"]

    gpu_data = json_data["Children"][0]["Children"][3]["Children"]
    gpu_temp = gpu_data[3]["Children"][0]["Value"]
    gpu_util = gpu_data[4]["Children"][0]["Value"]

    fan_data = json_data["Children"][0]["Children"][0]["Children"][0]["Children"][3]["Children"]
    avg_fan_spd = (remove_percent_space(fan_data[0]["Value"]) + remove_percent_space(fan_data[1]["Value"]) + remove_percent_space(fan_data[2]["Value"])) / 3
    # return {"cpu_temp": cpu_temp, "cpu_util": cpu_util, "gpu_temp": gpu_temp, "gpu_util": gpu_util}
    print("fan speed: " + avg_fan_spd)
    return json.dumps(gpu_data[4]["Children"][0]["Value"], indent=4)


# TODO: Add functions to strip spaces from inputs from lhm, also add leading 0s/spaces to fill out 20 chars per line
#  for the display
# sp_util_fan = f"{}%  {} RPM  {}%"
# ser.write(b"{sp_status}{}* CPU  GPU {}*{}")


if __name__ == "__main__":
    print(comp_get_stats())
