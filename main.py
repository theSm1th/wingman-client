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

    return {"cpu_temp": cpu_temp, "cpu_util": cpu_util,
            "gpu_temp": gpu_temp, "gpu_util": gpu_util,
            "avg_fan_spd": avg_fan_spd}


if __name__ == "__main__":
    data = comp_get_stats()
    print(data)
    header = "WINGMAN             "
    sp_util_fan = "{}%  {} RPM  {}%".format(lead_spacing(data["cpu_util"], 3, " "),
                                            lead_spacing(data["avg_fan_spd"], 4, " "),
                                            lead_spacing(data["gpu_util"], 3, " "))

    sp_temps = "{}C CPU    GPU {}C".format(lead_spacing(data["cpu_temp"], 3, " "),
                                           lead_spacing(data["gpu_temp"], 3, " "))
    flavour_text = "Blast Processing..."
    string_to_write = f"{header}{sp_util_fan}{sp_temps}{flavour_text}"
    ser.write(string_to_write.encode())
