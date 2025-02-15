[LIBBND_CKTPY]: <https://circuitpython.org/libraries>

## `MediaHub_AFMacropad`: Installation instructions
<!----------------------------------------------------------------------------->

# Uploading sample project to a microcontroller
<!----------------------------------------------------------------------------->

## Install the CircuitPython environment
<!----------------------------------------------------------------------------->
Before uploading the python code, you must install a copy of CircuitPython from Adafruit.

1. Download .uf2 file here (v9.2.1 tested):
   - <https://circuitpython.org/board/adafruit_macropad_rp2040/>

2. Upload the .uf2 file to your RP2040 macropad:
   - Plug in macropad USB to your PC while holding the BOOTSEL button (rotary encoder).
   - A new `[drive:]` should get mounted on your system.
   - Drag/drop downloaded .uf2 file onto newly mounted `[drive:]` (RPI-RP2).

## Uploading: using python script (optional/alternate)
<!----------------------------------------------------------------------------->
An optional install script is provided in [.\1-PkgUpload\pkg_upload.py](./1-PkgUpload/pkg_upload.py).

To have the script automatically upload contents of a "CircuitPython Library Bundle"
already unzipped on your system, you must un-comment the `LIBPATH_CPYBUNDLE`
environment variable and set it to this path.

1. Set `DEST_DRIVE` variable to point to your specific microcontroller.
2. Make sure `pkg` is set to the correct install package (`"MediaHub_AFMacropad"` in this case)
3. Run the `pkg_upload.py` script

That's it! You can skip the manual upload sections below if the script works for you.

## Uploading: Dependencies/required libraries
<!----------------------------------------------------------------------------->
From "CircuitPython Library Bundle" ([Download here][LIBBND_CKTPY]):
- Copy from bundle .zip file to the microcontroller `[drive:]\lib\` folder:
  - `adafruit_hid`
  - `neopixel.mpy`

From this repo's `MediaController` folder (1 level above):
- Copy all modules from `[..]\MediaController\lib_cktpy\*` => `[drive:]\lib\`
- Copy all modules from `[..]\MediaController\libpython\*` => `[drive:]\lib\`

## Uploading: Main code
<!----------------------------------------------------------------------------->
- Copy all python files `[.]\MediaHub_AFMacropad\*.py` => `[drive:]\`
