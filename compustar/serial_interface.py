import serial
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
)


class FirstechRemote:

    FT_HEADER = "0c0e03"
    FT_TERMINATOR = "0d"

    _incoming_buffer = ""

    class Command:

        COMMANDS = {
            "30": "LOCK",
            "31": "UNLOCK",
            "39": "TRUNK",
            "3a": "REMOTE_START",
            "34": "HOLD_TRUNK",
            "32": "HOLD_REMOTE_START",
            "a7": "LOCK_AND_UNLOCK",
            "a8": "LOCK_AND_TRUNK",
            "ab": "LOCK_AND_RS",
            "a9": "UNLOCK_AND_TRUNK",
            "ac": "UNLOCK_AND_RS",
            "ad": "TRUNK_AND_RS",
            "b4": "HOLD_LOCK_AND_TRUNK",
            "aa": "HOLD_TRUNK_AND_RS"
        }

        def __init__(self, command_id, decoder_id, remote_id):
            self.command_id = command_id
            self.decoder_id = decoder_id
            self.remote_id = remote_id

        def get_command_id(self):
            return self.command_id

        def get_command_text(self):
            return self.COMMANDS[self.command_id]

        def get_decoder_id(self):
            return self.decoder_id

        def get_remote_id(self):
            return self.remote_id

    def __init__(self):
        pass

    def setup(self, serial_port):
        self._ft_serial = serial.Serial(serial_port, 9600, timeout=1)
        logging.debug("Decoder Link Initialized")

    def on_command(self, fn):
        self._on_command = fn


    def _update_buffer(self):
        while self._ft_serial.in_waiting > 0:
            raw_data = self._ft_serial.read(self._ft_serial.in_waiting)
            self._incoming_buffer += raw_data.encode("hex")
        # logging.debug(self._incoming_buffer)

    def _termination_index(self, data):
        for i in range(0, len(self._incoming_buffer), 2):
            if data[i:i+2] == self.FT_TERMINATOR:
                return i
        return -1


    def listen(self):
        try:
            while(True):
                self._update_buffer()

                # Slice off anything before header
                header_position = self._incoming_buffer.find(self.FT_HEADER)
                if(header_position > -1):
                    self._incoming_buffer = self._incoming_buffer[header_position:]

                # Determine if termination character has arrived
                terminator_position = self._termination_index(self._incoming_buffer)
                if(terminator_position > -1):

                    # Store current command
                    current_command = self._incoming_buffer[0:terminator_position+2]

                    # Remove current command from buffer
                    self._incoming_buffer = self._incoming_buffer[terminator_position+2:]

                    if current_command[6:8] in self.Command.COMMANDS.keys():

                        self._on_command(
                            self.Command(
                                current_command[6:8],
                                current_command[8:10],
                                current_command[10:16]
                            )
                        )
                    else:
                        logging.debug(current_command)

        except KeyboardInterrupt:
            pass
        finally:
            self._ft_serial.close()
            logging.debug("Stopped")
