[LIB_ADA_HID]: <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
[LIB_CKTPY_PULSEIO]: <https://docs.circuitpython.org/en/latest/shared-bindings/pulseio/>
[IRRMT_LG_COMPAT]: <https://www.amazon.ca/dp/B0BHT5BW41>
[IRRMT_ADA]: <https://www.adafruit.com/product/389>
[ADABRD_RP2040MPAD]: <https://www.adafruit.com/product/5100>
[ADALRN_RP2040MPAD]: <https://learn.adafruit.com/adafruit-macropad-rp2040>
[ADALRN_KB2040]: <https://learn.adafruit.com/adafruit-kb2040>

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

## MediaHub: microcontroller packages
<!----------------------------------------------------------------------------->
- [`MediaHub_AFMacropad`](MediaHub_AFMacropad/): Media control.
  - Targets [Adafruit RP2040 Macropad][ADABRD_RP2040MPAD] board.
  - (Optional) Works with [Adafruit mini remote control (ID 389)][IRRMT_ADA] or [LG-compatible remote HERE][IRRMT_LG_COMPAT] (Good responsiveness).
  - NOTE: IR remote add-on requires modifying a STEMMA-QT cable to connect to an IR receiver module (more advanced).
  - [💾 List of files/libs to install](MediaHub_AFMacropad/pydrv_install.toml)
  - [🚀 Installation instructions](./1-INSTALL.md)
  - Tested on Windows/Android/Linux.

## MediaHub 2.0: microcontroller packages
<!----------------------------------------------------------------------------->
- [`MediaHub2p0_AFMacropad`](MediaHub2p0_AFMacropad/): Media control + extra large volume knob on STEMMA-QT port.
  - Targets [Adafruit RP2040 Macropad][ADABRD_RP2040MPAD] board.
  - [💾 List of files/libs to install](MediaHub2p0_AFMacropad/pydrv_install.toml)
  - [🚀 Installation instructions](./1-INSTALL.md)
  - Tested on Windows/Android/Linux.
- [`MediaHub2p0_KB2040`](MediaHub2p0_KB2040/): Optional IR remote receiver.
  - Targets [Adafruit Kee Boar][ADALRN_KB2040] board.
  - Extra microcontrolller needed since large volume knob (encoder) used in the main package (above) takes up the macropad's last remaining port.
  - Code works with [Adafruit mini remote control (ID 389)][IRRMT_ADA] or [LG-compatible remote HERE][IRRMT_LG_COMPAT] (Good responsiveness).
  - [💾 List of files/libs to install](MediaHub2p0_KB2040/pydrv_install.toml)
  - [🚀 Installation instructions](./1-INSTALL.md)
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
- [(DOCS) `CelIRcom` library](../../lib_cktpy/CelIRcom/1-README.md)
- [(DOCS) Adafruit HID library (USB Human Interface Devices)][LIB_ADA_HID]
- [(DOCS) Adafruit MacroPad RP2040][ADALRN_RP2040MPAD]: How to setup/assemble your macropad.
- [(DOCS) CircuitPython pulseio module][LIB_CKTPY_PULSEIO]
- [More on IR communications/decoding](../../lib_cktpy/CelIRcom/1-Resources.md)
