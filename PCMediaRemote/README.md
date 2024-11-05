[LIBBND_CKTPY]: <https://circuitpython.org/libraries>
[LIB_ADA_HID]: <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
[LIB_CKTPY_PULSEIO]: <https://docs.circuitpython.org/en/latest/shared-bindings/pulseio/>
[IRRMT_LG_COMPAT]: <https://www.amazon.ca/dp/B0BHT5BW41>
[IRRMT_ADA]: <https://www.adafruit.com/product/389>
## `PCMediaRemote`: A CircuitPython project
<!----------------------------------------------------------------------------->
Media remote receiver for your PC/MAC/thing supporting keyboard media keys.
- Also works with many smart TVs and phones.
- Flexible CircuitPython-based solution can easily be adapted to other microcontrollers/IR remotes.
- Built-in IR signal decoder utility on serial monitor output.
- An easy, inexpensive, solderless build! (if desired)

## More...
<!----------------------------------------------------------------------------->
- Send any keys supported by `adafruit_hid` lib (not just media keys).
- Requires CircuitPython: `pulseio` lib (not available for all microcontrollers).

## Provided/tested configuration
<!----------------------------------------------------------------------------->
- Targets Raspberry Pi Pico RP2040 board.
- Works with [Adafruit mini remote control (ID 389)][IRRMT_ADA].
- Works with [LG-compatible remote HERE][IRRMT_LG_COMPAT] (Good responsiveness).
- Tested on Windows/Mac/Linux.

# Uploading to a microcontroller (installation)
<!----------------------------------------------------------------------------->

## Uploading: Install CircuitPython environment
<!----------------------------------------------------------------------------->
Download .uf2 file here (v9.2.0 tested):
- <https://circuitpython.org/board/raspberry_pi_pico/>

Plug in USB to RP2040 board while holding the BOOTSEL button.
- A new `[drive:]` should get mounted on your system.
- Drag/drop downloaded .uf2 file onto newly mounted `[drive:]` (RPI-RP2).

## Uploading: Dependencies/required libraries
<!----------------------------------------------------------------------------->
- From "CircuitPython Library Bundle" ([Download here][LIBBND_CKTPY])
  - Copy from bundle .zip file to the microcontroller `[drive:]\lib\` folder:
    - `adafruit_hid`
- From this `[PCMediaRemote]` folder:
  - Copy all modules from `[PCMediaRemote]\lib_cktpy\*` => `[drive:]\lib\`

## Uploading: Main code
<!----------------------------------------------------------------------------->
The [`[PCMediaRemote]\pkg_install`](pkg_install/) folder contains separate
install packages for different project versions/examples.

Here is a listing of the available packages:
- `PKGFLD` = [`MediaRemote_RP2040`](pkg_install/MediaRemote_RP2040/1-ABOUT.md): Runs on Raspberry Pi Pico RP2040 board.

To upload one of the above `PKGFLD` packages, copy custom project code to the
microcontroller `[drive:]`:
- `[PCMediaRemote]\pkg_install\[PKGFLD]\*` => `[drive:]`
- ==> Can try automated script [pkg_upload.py](pkg_install/1-PkgUpload/pkg_upload.py)
  (also uploads `lib_cktpy\*` modules).

# ⚠️ Known issues
<!----------------------------------------------------------------------------->
- SAMD21 boards: Typically do not support `pulseio` (required library). Also has insufficient memory (compile to `.mpy`?).
- Circuit Playground Bluefruit: Works - but somewhat sluggish. Needs optimization.

TODO:
- `CelIRcom` library dynamically allocates memory (inefficient). Preferable to use static arrays instead.
- Provide `.mpy` (compiled) lib?

# Additional resources/links
<!----------------------------------------------------------------------------->
- [DOCS: `CelIRcom` library](lib_cktpy/CelIRcom/1-README.md)
- [DOCS: CircuitPython pulseio module][LIB_CKTPY_PULSEIO]
- [DOCS: Adafruit HID library (USB Human Interface Devices)][LIB_ADA_HID]
- [More on IR communications/decoding](lib_cktpy/CelIRcom/1-Resources.md)
