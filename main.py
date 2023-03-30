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
    return json.dumps(cpu_data[3]["Children"][0]["Value"], indent=4)

# sp_util_fan = f"{}%  {} RPM  {}%"
# ser.write(b"{sp_status}{}* CPU  GPU {}*{}")


if __name__ == "__main__":
    print(comp_get_stats())
