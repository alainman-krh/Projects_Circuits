[CPY_LIBS]: <https://circuitpython.org/libraries>
[LG_IRRMT_COMPAT]: <https://www.amazon.ca/dp/B0BHT5BW41>
[ADA_IRRMT]: <https://www.adafruit.com/product/389>
## `RP2040_MediaRemote`: A CircuitPython project
<!----------------------------------------------------------------------------->
Turn your microcontroller board into a media remote receiver for your PC/Mac.

# Features
<!----------------------------------------------------------------------------->
- Modifiable to use any IR remote.
- Can send any keys supported by `adafruit_hid` lib (not just media keys).

# Provided/tested configuration
<!----------------------------------------------------------------------------->
- Pre-configured for Raspberry Pi Pico RP2040 board.
- Preset to work with [Adafruit mini remote control (ID 389)][ADA_IRRMT].
- Preset to work with [LG-compatible remote HERE][LG_IRRMT_COMPAT] (Good responsiveness).
- Tested on Windows/Mac/Linux.

# Installing CircuitPython environment
Download .uf2 file here (v9.0.0 tested):
- <https://circuitpython.org/board/raspberry_pi_pico/>

Plug in USB to RP2040 board while holding the BOOTSEL button.
- A new drive should get mounted on your system.
- Drag/drop downloaded .uf2 file onto newly mounted drive (RPI-RP2).

# Installation/requirements
<!----------------------------------------------------------------------------->
- CircuitPython (Tested: v9.0.0)
- From "CircuitPython Library Bundle" ([Download here][CPY_LIBS])
  - Copy from bundle .zip file to the microcontroller `[drive:]\lib\` folder:
    - `adafruit_hid`

Copy custom project code to microcontroller `[drive:]`:
- `PCMediaRemote\lib_cktpy\*` => `[drive:]\lib\`
- `.\*.py` => `[drive:]\`
- ==> Can use automated script `pkg_upload.py` in [../1-PkgUpload/](../1-PkgUpload/)

# Comments
<!----------------------------------------------------------------------------->
- Should work on any microcontroller supported by the CircuitPython `pulseio` lib (not just RP2040).

# Resources/Links
<!----------------------------------------------------------------------------->
- <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
