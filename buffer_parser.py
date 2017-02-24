import serial
import logging
import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )



class FirstechRemote:

    FT_HEADER = '0c0e03'  # Form Feed/Page Break (0x0c == FF); Shift out (0x0e == SO); End-of-text (0x03 == ETX) (Why not STX?)
    FT_TERMINATING = '0d'  # Just a LF

    _incoming_buffer = []

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
            "b4": "HOLD_LOCK_AND_TRUNK"
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

    def _update_buffer(self):
        while self.ft_serial.in_waiting > 0:

            raw_data = self.ft_serial.read(self.ft_serial.in_waiting)
            hex_data = raw_data.encode("hex")

            for i in range(0, len(hex_data)):
                self._incoming_buffer.append(hex_data[i:i+1])

    def _buffer_not_empty:
        return len(self._incoming_buffer) > 1

    def on_command(self, fn):
        self._on_command = fn


    def get_command(self):
        temp_buffer = ""
        found_terminator = False
        while(not found_terminator):
            new_chunk = self._incoming_buffer.pop(0)
            temp_buffer += new_chunk
            if new_chunk == FT_TERMINATING:
                found_terminator = True
        header_pos = temp_buffer.find(self.FT_HEADER)
        temp_buffer = temp_buffer[header_pos:]
        # return Command(temp_buffer[6:8], temp_buffer[8:10], temp_buffer[10:16])
        return Command(temp_buffer[3], temp_buffer[4], temp_buffer[5:8].join(""))

    def listen(self):
        try:
            while(True):
                self._update_buffer()
                if self._buffer_not_empty():
                    self._on_command(get_command)
        except KeyboardInterrupt:
            pass



log_remote_data(command):
    print "Remote %s sent %s" % (command.get_remote_id, command.get_command_text())

ft_remote = FirstTechRemote()
ft_remote.setup("/dev/tty.usbserial-AD012345")
ft_remote.on_command(log_remote_data)
ft_remote.listen()
