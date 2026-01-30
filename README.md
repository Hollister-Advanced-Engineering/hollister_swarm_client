# Hollister Swarm Client – Raspberry Pi Pico Setup (CircuitPython)

This guide walks you through installing the required files on a **Raspberry Pi Pico** so it can run the Hollister Swarm Client using **CircuitPython**.

Follow the steps carefully and in order. If something doesn’t match what you see on your computer, stop and ask for help.

---

## What You’ll Need

- Raspberry Pi Pico (or Pico W)
- Micro-USB cable (data cable, not charge-only)
- A computer (Windows, macOS, or Linux)
- Internet access

---

## Step 1: Install CircuitPython on the Pico

1. **Unplug** your Raspberry Pi Pico.
2. Hold down the **BOOTSEL** button on the Pico.
3. While holding BOOTSEL, plug the Pico into your computer via USB.
4. Release the BOOTSEL button.

You should now see a new drive appear on your computer called:
```
RPI-RP2
```

5. Download the correct CircuitPython `.uf2` file:
   - https://circuitpython.org/board/raspberry_pi_pico/
   - (Use **Pico W** version if you are using WiFi)

6. Drag the downloaded `.uf2` file onto the `RPI-RP2` drive.

The Pico will automatically reboot.

✅ When finished, a new drive should appear called: 
```
CIRCUITPY
```

---

## Step 2: Download the Swarm Client Code

1. Go to the GitHub repository:
https://github.com/Hollister-Advanced-Engineering/hollister_swarm_client
2. Click **Code → Download ZIP**
3. Unzip the downloaded file.

Inside the folder, you should see:
```
code.py
lib/
README.md
(other files)
```


---

## Step 3: Copy `code.py` to the Pico

1. Open the `CIRCUITPY` drive.
2. If a file named `code.py` already exists, **replace it**.
3. Drag **`code.py`** from the repository folder into the root of `CIRCUITPY`.

After this step, `CIRCUITPY` should contain:
```
code.py
```


---

## Step 4: Copy the `lib` Folder

1. Open the `lib` folder from the repository.
2. Open the `lib` folder on the `CIRCUITPY` drive.
   - If it does not exist, create a folder named **lib**
3. Copy **all files and folders** from the repository’s `lib` directory into:
```
CIRCUITPY/lib
```


⚠️ Do NOT rename any library files.

---

## Step 5: Verify File Structure

Your `CIRCUITPY` drive should now look like this:
```
CIRCUITPY/
│
├── code.py
│
├── lib/
│ ├── adafruit_requests/
│ ├── adafruit_bus_device/
│ ├── adafruit_connection_manager.mpy
│ └── (other .mpy or folders)
```


If your structure does **not** match this, the code will not run.

---

## Step 6: Safely Eject and Reset

1. Safely eject the `CIRCUITPY` drive.
2. Unplug the Pico.
3. Plug it back in normally (no BOOTSEL).

The Pico will automatically run `code.py`.

---

## Troubleshooting

**Nothing happens**
- Check that `code.py` is spelled exactly right (lowercase)
- Verify libraries are inside `CIRCUITPY/lib`

**Red LED blinking / error**
- Open `CIRCUITPY` → `code.py`
- Look for missing libraries or syntax errors
- Ask an instructor before changing code

**No `CIRCUITPY` drive**
- CircuitPython may not be installed correctly
- Repeat Step 1

---

## Rules of Thumb

- CircuitPython runs **automatically** when the Pico powers on
- Editing `code.py` updates behavior instantly on save
- If it’s not in `lib/`, CircuitPython can’t import it

---

You’re now ready to run the Hollister Swarm Client 🚀


