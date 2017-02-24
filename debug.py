import serial

# Serial data comes in an looks like this:
# 0c0e0331038e9971ea0d
#
# Broken up we get this:
#   Blocks:         [0c0e03]   [310]    [3]     [8e9971]    [xx]        [0d]
#   Description:    HEADER      CMD     '3'     Remote ID   Checksum    Terminator
#   Length:         6           3       1       6           2           2
#   Positions:      1 - 6       7-9     10      11-16      17-18       19-20
#
# #### Commands in Hex-notation
#
# # Single Presses
# FT_LOCK                 = "300"
# FT_UNLOCK               = "310"
# FT_TRUNK                = "390"
# FT_REMOTE_START         = "3a0"
#
# # Single HOLD
# FT_HOLD_TRUNK           = "340"
# FT_HOLD_REMOTE_START    = "320"
#
# # Two-key press
# FT_LOCK_AND_UNLOCK      = "a70"
# FT_LOCK_AND_TRUNK       = "a80"
# FT_LOCK_AND_RS          = "ab0"
# FT_UNLOCK_AND_TRUNK     = "a90"
# FT_UNLOCK_AND_RS        = "ac0"
# FT_TRUNK_AND_RS         = "ad0"
#
# # Two-key hold
# FT_HOLD_LOCK_AND_TRUNK  = "b40"
#
#
# Full details of data sent by both remotes
# The last two characters might be a checksum and are unique to each type of command sent
#   2WG9R-SP:
#   8e9971dc
#   8e9971dd
#   8e9971e5
#   8e9971e6
#   8e9971de
#
#   1WG9R-SP:
#   7ff230e5
#   7ff230e6
#   7ff230ee
#   7ff230ef
#   7ff230e7
#   7ff230e9
#
# For basically no reason at all, this is sent before any commands come in
# 000c0eff00000d0d
#

class FirstTechRemotes:

    FT_HEADER = "0c0e03"

    REMOTE_COMMANDS = {
        768: "LOCK",
        784: "UNLOCK",
        912: "TRUNK",
        928: "REMOTE_START",
        832: "HOLD_TRUNK",
        800: "HOLD_REMOTE_START",
        2672: "LOCK_AND_UNLOCK",
        2688: "LOCK_AND_TRUNK",
        2736: "LOCK_AND_RS",
        2704: "UNLOCK_AND_TRUNK",
        2752: "UNLOCK_AND_RS",
        2768: "TRUNK_AND_RS",
        2720: "HOLD_TRUNK_AND_RS",
        2880: "HOLD_LOCK_AND_TRUNK"
    }

    # Everything ends with
    FT_TERMINATING = "0d"


    def __init__(self, serial_port, trusted_remotes):
        self.incoming_buffer = ""
        self.trusted_remotes = trusted_remotes
        self.ft_serial = serial.Serial(serial_port, 9600, timeout=1)
        print "Decoder Link Initialized"

    def interpret_command(self, raw_remote_data):
        if self.FT_HEADER in raw_remote_data and self.FT_TERMINATING in raw_remote_data and len(raw_remote_data) >= 20:
            # Probably useful!
            ft_start_index = raw_remote_data.find(self.FT_HEADER)
            ft_cmd = raw_remote_data[ft_start_index:ft_start_index+20]
            if ft_cmd[18:] == self.FT_TERMINATING:
                # Header and footer look good
                remote_id = ft_cmd[10:16]
                print remote_id
                # if remote_id in self.trusted_remotes:
                    # Remote has been verified
                return ft_cmd[6:9]

    def append_to_buffer(self, new_hex_data):
        self.incoming_buffer += new_hex_data

    def update(self):
        while self.ft_serial.in_waiting > 0:

            new_data = self.ft_serial.read(self.ft_serial.in_waiting)

            self.append_to_buffer(
                    new_data.encode("hex")
            )


    def get_command(self):
        if len(self.incoming_buffer) >= 20:
            print "RAW: %s" % self.incoming_buffer
            raw_cmd_buffer_start = self.incoming_buffer.find(self.FT_HEADER)
            raw_cmd_buffer_end = raw_cmd_buffer_start + 20

            if raw_cmd_buffer_start >= 0 and raw_cmd_buffer_end <= len(self.incoming_buffer): # Check to see if a full command could possibly be in the buffer
                # if raw_cmd_buffer[9] == "3" and raw_cmd_buffer[raw_cmd_buffer_end-2:raw_cmd_buffer_end] == FT_TERMINATING:
                    # Promising!
                probably_valid_cmd_buffer = self.incoming_buffer[raw_cmd_buffer_start:raw_cmd_buffer_end] # Grab what should be a good command
                self.incoming_buffer = self.incoming_buffer[raw_cmd_buffer_end:] # Remove remove it and any garbage from the beginning

                remote_command = int(self.interpret_command(probably_valid_cmd_buffer), 16) # Hex back to decimal
                return remote_command

# 8e9971 & 7ff230 are 2-way remotes
# e5f3a0 = FTX1WR1R-AM (1-BAM equivalent)

ft_remote_decoder = FirstTechRemotes("/dev/tty.usbserial-AD012345", ["8e9971", "7ff230"])

import os

while(True):
    ft_remote_decoder.update()

    remote_command = ft_remote_decoder.get_command()
    # if remote_command is not None:
    #
    #     if remote_command in FirstTechRemotes.REMOTE_COMMANDS.keys():
    #         print FirstTechRemotes.REMOTE_COMMANDS[remote_command]
    #     else:
    #         print remote_command
