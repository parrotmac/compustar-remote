import requests

from compustar.serial_interface import FirstechRemote

# !IMPORTANT! You'll need to change this string to reference your own light(s)
color_hue_endpoint = 'http://<bridge ip address>/api/1028d66426293e821ecfd9ef1a0731df/lights/4/state'

HUE_STATES = {
    "OFF": {
        "on": False
    },
    "RED": {
        "on": True,
        "sat":254,
        "bri": 255,
        "xy": [
			0.6831,
			0.2919
		]
    },
    "WHITE": {
        "on":True,
        "sat":254,
        "bri":255,
        "xy": [
            0.3146,
            0.3304
        ]
    },
    "BLUE": {
        "on": True,
        "sat":254,
        "bri": 255,
        "xy": [
			0.1788,
			0.1991
		]
    }
}

def contact_hue_bridge(new_state):
    hue_request = requests.put(color_hue_endpoint, json=new_state)
    print(hue_request.json())


def control_hue(command):
    if command.get_command_text() == "LOCK":
        contact_hue_bridge(HUE_STATES['RED'])

    elif command.get_command_text() == "UNLOCK":
        contact_hue_bridge(HUE_STATES['WHITE'])

    elif command.get_command_text() == "TRUNK":
        contact_hue_bridge(HUE_STATES['BLUE'])

    else:
        contact_hue_bridge(HUE_STATES['OFF'])

    # Lil' helpful debugging info
    print("Remote %s sent %s" % (command.get_remote_id(), command.get_command_text()))


compustar_remote = FirstechRemote()
compustar_remote.setup("/dev/tty.usbserial-AD012345")
compustar_remote.on_command(control_hue)
compustar_remote.listen()
