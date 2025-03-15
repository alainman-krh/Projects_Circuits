[LIBBND_CKTPY]: <https://circuitpython.org/libraries>

## `MediaController`: Installation instructions
<!----------------------------------------------------------------------------->

# Uploading a sample package to your microcontroller
<!----------------------------------------------------------------------------->

## ✔️ Install the CircuitPython environment (manual)
<!----------------------------------------------------------------------------->
Before uploading the python code, you must install a copy of CircuitPython from Adafruit.

1. Download .uf2 file for the board of interest here (v9.2.1 tested):
   - <https://circuitpython.org/board/adafruit_macropad_rp2040/>
   - <https://circuitpython.org/board/adafruit_kb2040/>
   - You can search for a different board if adapting the sample code.

2. Upload the .uf2 file to your microcontroller:
   - Plug in macropad USB to your PC while holding the BOOTSEL button (rotary encoder on the RP2040 macropad).
   - A new `[drive:]` should get mounted on your system.
   - Drag/drop downloaded .uf2 file onto newly mounted `[drive:]` (RPI-RP2).

## ✔️ Uploading with the provided python script (suggested)
<!----------------------------------------------------------------------------->
An optional install script is provided in [.\1-PkgUpload\pkg_upload.py](./1-PkgUpload/pkg_upload.py).
- [pkg_upload: README](./1-PkgUpload/README.md)

To have the script automatically upload contents of a "CircuitPython Library Bundle"
([Download here][LIBBND_CKTPY]), you must un-comment the `LIBPATH_CPYBUNDLE`
environment variable and set it to the unzipped library bundle path.

1. Set `DEST_DRIVE` variable to point to your specific microcontroller.
2. Make sure `pkg` is set to the correct install package (ex: `"MediaHub_AFMacropad"`)
3. Run the `pkg_upload.py` script

That's it! You can skip the manual upload sections below if the script works for you.

# 🎉️🎉️🎉️🎉️

# ⚠️ Alternate install: Manually uploading code to your microcontroller
<!----------------------------------------------------------------------------->
Subdirectories of this folder contain individual sample packages that can be
uploaded to your microcontroller. We'll use `$PKGFLD` to identify that folder.

Each package has a listing of required files to be installed in a `.toml` (text) file:
- `$PKGFLD\pydrv_install.toml`

## Uploading dependencies/required libraries (manual)
<!----------------------------------------------------------------------------->
From "CircuitPython Library Bundle" ([Download here][LIBBND_CKTPY]):
- Unzip the library bundle to a temporary directory on your local drive (`$LIBUNZIPPED`).
- Copy all files/folders listed in the `[modules.CPYBUNDLE]` section of
  `$PKGFLD\pydrv_install.toml` to your microcontroller's `[drive:]\lib\` folder.
- These files/folders should be present in the `$LIBUNZIPPED\lib` folder.

From this repo's `$PROJROOT = [..]\MediaController` folder (1 level above):
- Copy all folders listed in the `[modules]` section of `$PKGFLD\pydrv_install.toml`
  to your microcontroller's `[drive:]\lib\` folder as well.

## Uploading the main code (manual)
<!----------------------------------------------------------------------------->
- Copy all folders listed in the `[package]` section of `$PKGFLD\pydrv_install.toml`
  to your microcontroller's `[drive:]\` folder.

## Try it out!
Reset your microcontroller board, and see if it works!