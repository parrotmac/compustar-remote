# Python Compustar Remote
This is an example of how to interface Compustar/Firstech remotes from within Python.
See the hookup guide below for connection details.

A command hex-encoded from a decoder module will give you something like this:
`0c0e0331xxyyyyyyzz0d`. This is an `UNLOCK` command from a remote id `yyyyyy` using a decoder `xx`.
Details are broken down in this table:
```
Blocks:         0c0e03      31      xx          yyyyyy      zz          [2000]      0d
Description:    HEADER      CMD     Decoder     Remote ID   Checksum    [Unkown*]   Terminator
Length:         6           2       2           6           2           [4]         2
Positions:      1 - 6       7-8     9-10        11-16       17-18       [19-20]     19-20 or 23-26
```
The `unknown` block is only returned by one FT-100/CS2 decoder, but not the other. It's unknown what this field does, other than make the command length more unpredictable :P

## Header
`0c` `0e` `03`
- Form Feed/Page Break (0x0c == FF)
- Shift out (0x0e == SO)
- End-of-text (0x03 == ETX)

## Commands
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

## Terminator
`0d`
This is just a CR (\r)

---

## Disclaimer: ##
This project is in no way sponsored or endoresed by Firstech LLC or any of its brands or subsidiaries.

