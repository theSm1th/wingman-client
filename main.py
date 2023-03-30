import serial
import requests
import json


# ser = serial.Serial("COM9", 9600, timeout=0.05)
# ser.write(b"WINGMAN             00.0* CPU  GPU 00.0*100%  1000 RPM  100%####################")

def format_temp(to_format):
    if to_format >= 100:
        return "OVERL"
    return "{:.1f}*".format(to_format)


def comp_get_stats():
    data_get = requests.get("http://localhost:8085/data.json")
    json_data = json.loads(data_get.content)

    cpu_data = json_data["Children"][0]["Children"][1]["Children"]
    cpu_temp = cpu_data[3]["Children"][0]["Value"]
    cpu_util = cpu_data[4]["Children"][0]["Value"]

    gpu_data = json_data["Children"][0]["Children"][3]["Children"]
    gpu_temp = json_data
    gpu_util = gpu_data # TODO: Finish this on computer - Xe does not show aggregated util
    return {"cpu_temp":cpu_temp, "cpu_util":cpu_util, "gpu_temp":gpu_temp, "gpu_util": gpu_util}
    #return json.dumps(cpu_data[4]["Children"][0]["Value"], indent=4)

# TODO: Add functions to strip spaces from inputs from lhm, also add leading 0s/spaces to fill out 20 chars per line
#  for the display
# sp_util_fan = f"{}%  {} RPM  {}%"
# ser.write(b"{sp_status}{}* CPU  GPU {}*{}")


if __name__ == "__main__":
    print(comp_get_stats())
