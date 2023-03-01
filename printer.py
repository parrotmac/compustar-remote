from compustar.serial_interface import FirstechRemote
import subprocess


def on_command(command):
    print(f"Remote({command.get_remote_id()})\tCommand({command.get_command_id()}): {command.get_command_text()}")
    cmd_text = command.get_command_text()
    subprocess.run(
        "say",
        input=cmd_text.encode("utf-8"),
        capture_output=True,
    )

    # print(command.get_command_text())

def main():
    remote = FirstechRemote()
    remote.setup("/dev/tty.usbserial-AD012345")
    remote.on_command(on_command)
    remote.listen()

if __name__ == "__main__":
    main()
