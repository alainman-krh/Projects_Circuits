[LIB_ADA_HID]: <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
[LIB_CKTPY_PULSEIO]: <https://docs.circuitpython.org/en/latest/shared-bindings/pulseio/>
[IRRMT_LG_COMPAT]: <https://www.amazon.ca/dp/B0BHT5BW41>
[IRRMT_ADA]: <https://www.adafruit.com/product/389>
[ADABRD_RP2040MPAD]: <https://www.adafruit.com/product/5100>
[ADALRN_RP2040MPAD]: <https://learn.adafruit.com/adafruit-macropad-rp2040>

# `MediaController`: CircuitPython-powered projects
<!----------------------------------------------------------------------------->
Build-your-own media control surface with CircuitPython-powered microcontrollers.
- Connect to your phone/PC/MAC/thing supporting keyboard media keys.
- Flexible CircuitPython-based solution can easily be adapted to other microcontrollers/IR remotes.
- Includes simple solderless build examples!

## More...
<!----------------------------------------------------------------------------->
- Send any keys supported by `adafruit_hid` lib for media control (not just media keys).
- Optional IR control requires CircuitPython `pulseio` lib (not available for all microcontrollers).

## Variants
<!----------------------------------------------------------------------------->
- [`MediaHub_AFMacropad`](MediaHub_AFMacropad/): Media control w/opt Bluetooth using [Adafruit RP2040 Macropad][ADABRD_RP2040MPAD].
  - [🚀 Installation instructions](../pkg_install/INSTALL_AFMacropad.md)

## Provided/tested configuration
<!----------------------------------------------------------------------------->
[`MediaHub_AFMacropad`](MediaHub_AFMacropad/) targets [Adafruit RP2040 Macropad][ADABRD_RP2040MPAD] board:
- (Optional) Works with [Adafruit mini remote control (ID 389)][IRRMT_ADA].
- (Optional) Works with [LG-compatible remote HERE][IRRMT_LG_COMPAT] (Good responsiveness).
- Tested on Windows/Android/Linux.

# ⚠️ Known issues
<!----------------------------------------------------------------------------->
TODO:
- `CelIRcom` library dynamically allocates memory (inefficient). Preferable to use static arrays instead.
- Provide `.mpy` (compiled) lib?
- Look for NOALLOC, `ptrain???_build`
- Does gc.collect() help or hinder???

# Additional resources/links
<!----------------------------------------------------------------------------->
- [(DOCS) `CelIRcom` library](../lib_cktpy/CelIRcom/1-README.md)
- [(DOCS) Adafruit HID library (USB Human Interface Devices)][LIB_ADA_HID]
- [(DOCS) Adafruit MacroPad RP2040][ADALRN_RP2040MPAD]: How to setup/assemble your macropad.
- [(DOCS) CircuitPython pulseio module][LIB_CKTPY_PULSEIO]
- [More on IR communications/decoding](../lib_cktpy/CelIRcom/1-Resources.md)
