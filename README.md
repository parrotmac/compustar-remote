# Python Compustar Remote
This is an example of how to interface Compustar/Firstech remotes using Python.
See the hookup guide below for connection details.

Watch: [Vido demonstration of using a Compustar remote to control a Philips Hue color light (YouTube)](https://www.youtube.com/watch?v=nWA2bXaIzMM)

# Command Structure

A hex-encoded message from a decoder might look like this:
`0c0e0331xxyyyyyyzz0d`. This is an "UNLOCK" command from remote id `yyyyyy` using decoder `xx`.
This example is broken down in this table:
```
Blocks:         0c0e03      31        xx          yyyyyy      zz          [2000]      0d
Description:    Header      Command   Decoder     Remote ID   Checksum    [Unkown*]   Terminator
Length:         3           1         1           3           1           [2]         1
Offset:         0 - 2       3         4           5 - 7       8           [9 - 10]    9 [or 11]
```
Of the two FT-100/CS2 decoder decoders tested, one adds what I've labeled `unknown`. I have no idea what this data means or does, other than it making the command length more unpredictable :P

### Header
`0c0e03`
Possible interpretations:
- Form Feed/Page Break (`0x0c` == FF)
- Shift out (`0x0e` == SO)
- End-of-text (`0x03` == ETX)

### Commands
Descriptions of each of the commands
- Single key press
    - LOCK                 = `30`
    - UNLOCK               = `31`
    - TRUNK                = `39`
    - REMOTE_START         = `3a`
- Single key hold
    - HOLD_TRUNK           = `34`
    - HOLD_REMOTE_START    = `32`
- Two-key press
    - LOCK_AND_UNLOCK      = `a7`
    - LOCK_AND_TRUNK       = `a8`
    - LOCK_AND_RS          = `ab`
    - UNLOCK_AND_TRUNK     = `a9`
    - UNLOCK_AND_RS        = `ac`
    - TRUNK_AND_RS         = `ad`
- Two-key hold
    - HOLD_LOCK_AND_TRUNK  = `b4`
    - HOLD_TRUNK_AND_RS    = `aa`

### Decoder
Probably a unique ID of the decoder, but I don't have enough info to say definitively.

### Remote ID
Six bytes that change depending on which remote sent the command.

### Checksum
Consistent for a specific command and remote. CRC-based checksum perhaps?

### Unknown
As noted above, the purpose of this baffles me.

### Terminator
`0d`
This is just a CR (\r)

---

# Hookup Guide
Here's our target -- this is what we want to receive commands from
![Compustar remote](http://i.imgur.com/PDRMJU2.jpg)
For this example I'm using three main components:
![Hookup Guide Photo](http://i.imgur.com/KTe0ogO.jpg)
The items (bottom to top in the photo):
- Remote and Antenna (Compustar/Firstech RS-2WG9-SP) [Compustar Product Listing](https://www.compustar.com/remote-start/prime-g9), 
- Decoder Module (Compustar FT-100/iDatalink 2CS) [iDatalink's Product Listing](http://compustar.idatalink.com/accessories/category/product_id/86)
- RS232 Interface Cable (iDatalink Weblink Updater Cable) [iDatalink's Product Listing](http://www.idatalink.com/accessories/category/product_id/45)

#### Remote and Antenna
This is the whole point of this tomfoolery. The remote and antenna are usually found together, but they aren't really tied to one another. However, there are different types of both remotes and antennas. The pictured atenna (the part labeled ANT-2WSP) and remote (photo above) are 2-Way, meaning the antenna has the ability to send signals back to the remote. 2-Way functionality is not yet included in this project.
#### Decoder Module
**Important:** Newer Compustar 2-Way remotes *may* not need a decoder module, as the decryption happens inside the antenna module. That being said, I haven't verified that this setup will work with this new generation of antennas.

Most modern car fobs use some sort of encryption[CITATION NEEDED]. For whatever reason, despite known issues, it seems a common algorithm is KeeLoq. While I don't know for sure, based on FCC filing information I suspect these remotes are no different.

In this setup, the antenna module (ANT-2WSP) is sending information it receives from a remote over serial (?) in a still enctrypted form. Compustar remote start controllers (often dubbed *brains*) have built-in decoders that decrypt and interpret the commands. However, for reasons not discussed here, Compustar (or iDatalink, friends of Compustar) built the iDatalink 2CS/Compustar FT-100 decoder module that very conveniently decodes the (probably) KeeLoq encrypted data from the remotes, and spits out very usable information over RS232.
#### RS232 Interface Cable
This part is definitely not necessary. Instead, an Arduino and a 12V power source will work great. The photo below shows the connection to the decoder module, with 12V and GND being Red and black, respectively. The yellow and white wires are the data lines (RX/TX, maybe respectively 😉). It should be a 5V logic level, but please don't have your Arduino make that determination...
The is cable made for flashing firmware and upgrading iDatalink modules and Compustar remote start modules. It seems to be a pretty generic module, though. Under Linux and macOS it shows up as a generic RS232/Serial interface. It's probably just an FTDI (or similar) chip with a buck converter in a sleek package.
![CS2 Pinout](http://i.imgur.com/caOVMWB.jpg)

---
# FAQ and TODO

#### FAQ
**Q:** Do you have any frequently asked questions to answer here?

**A:** No.

#### TODO
-   Get 2-Way working
-   Confirm functionaly of newer Compustar remotes

---
# Disclaimer:
This project is not affiliated with Firstech LLC.

---
# License: MIT

```markdown
Copyright (c) 2017 Isaac Parker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
