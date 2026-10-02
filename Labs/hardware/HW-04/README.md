# HW-04: Raspberry Pi 5 image

Hardware status: not tested on hardware (prepared on 2026-10-01)

Needed by: the Day 7 lab and the Day 8 lab. Days 9 to 15 use the same card.

## Decision

| Topic | Decision |
|---|---|
| Operating system | Raspberry Pi OS (64-bit) with the desktop, written with Raspberry Pi Imager |
| User name | `edge`, the same on all cards. The instructor sets the password. |
| Host name | `pi-NN`, where `NN` is the group number. The master card is `pi-00`. |
| Remote access | SSH, enabled in Raspberry Pi Imager. Name `pi-NN.local`. |
| Python | Three virtual environments, each with `--system-site-packages`: `~/tflite_env`, `~/yolo`, `~/ollama` |
| Camera library | `picamera2` from `apt`, not from `pip` |
| Method for many cards | Prepare one master card. Copy it to all cards. Run `set_hostname.sh` one time on each copy. |

## Reason

- The book uses Raspberry Pi OS (64-bit) with the desktop for the Raspberry
  Pi 5. The guide for small language models says that a 32-bit operating
  system cannot run them.
- The companion book makes one environment for each area: `~/tflite_env`,
  `~/yolo`, and `~/ollama`. The course keeps these names, so the commands of
  the book work with no change. Separate environments also keep the package
  versions of one lab away from the other labs.
- The companion book gives this rule: use `apt` for system libraries and
  hardware libraries, and use `pip` in an environment for all other packages.
  `picamera2` talks to the camera hardware, so it comes from `apt`. The
  option `--system-site-packages` lets an environment see it.
- The setup needs large downloads (PyTorch, Ultralytics, Ollama). One master
  card and a copy are faster than the same setup on each card. All groups
  then have the same versions.
- A unique host name lets a group find its Raspberry Pi with no IP address.

The book also removes the file `EXTERNALLY-MANAGED` to permit `pip` with no
environment. The course does not do this, because all packages are in the
environments.

## Sources

| Item | Source |
|---|---|
| Operating system, Raspberry Pi Imager, SSH, shutdown, file transfer | Raspberry Pi setup chapter of "Machine Learning Systems" (`kits/contents/raspi/setup/setup.qmd`) |
| Camera commands (`--list-cameras`, `rpicam-jpeg`) | The same chapter, section "Installing a Camera Module on the CSI port" |
| Environments and packages | "Edge AI Engineering: Raspberry Pi", chapters "Image Classification Fundamentals", "Computer Vision Applications with YOLO", and "Small Language Models" |
| Rule for `apt` and `pip` | "Edge AI Engineering: Raspberry Pi", chapter "Setup" |
| Ollama install command, 64-bit rule, cooler | `A_Guide_to_Local_Inference/README.md` of "EdgeML with Raspberry Pi", section 5 |
| Temperature command | Small language model chapter of "Machine Learning Systems" |

## Files

| File | Runs on | Content |
|---|---|---|
| `setup_pi.sh` | master Raspberry Pi | Installs the system packages, the three environments, Ollama, and the network tools |
| `check_pi.sh` | each Raspberry Pi | Prints PASS or FAIL for the system, the camera, the environments, and the tools |
| `prepare_master.sh` | master Raspberry Pi | Cleans the card before the copy, then shuts down |
| `set_hostname.sh` | each copy | Sets `pi-NN`, makes new SSH keys and a new machine identity |

## Steps

### 1. Write the master card

1. Install Raspberry Pi Imager on the laptop (`www.raspberrypi.com/software`).
2. Select the device **Raspberry Pi 5** and the system
   **Raspberry Pi OS (64-bit)**.
3. Open the settings of the Imager before you write. Set:
   - host name: `pi-00`
   - user name: `edge`, and a password
   - Wi-Fi: the name and the password of the lab router (`HW-09`)
   - SSH: enabled, with password
   - time zone and keyboard layout
4. Write the card. Put it in the Raspberry Pi and connect the power.
5. Wait some minutes for the first start. Then connect:

   ```bash
   ssh edge@pi-00.local
   ```

   If the name does not work, read the IP address in the device list of the
   router and use `ssh edge@IP_ADDRESS`.

### 2. Connect the camera and the cooler

1. Remove the power first.
2. Install the active cooler. Connect its cable to the fan connector.
3. Connect the Camera Module 3 with the cable for the Raspberry Pi 5. The
   Raspberry Pi 5 has a smaller camera connector than older models.
4. Connect the power again.

The Camera Module 3 needs no change of `config.txt`. The operating system
finds it. The book changes `config.txt` only for other camera types.

### 3. Run the setup script

Copy this folder to the Raspberry Pi, then run the script:

```bash
scp -r Labs/hardware/HW-04 edge@pi-00.local:~/
ssh edge@pi-00.local
bash ~/HW-04/setup_pi.sh
```

The script writes its output to `~/setup_pi.log`. It installs these parts:

| Part | Content | Used on |
|---|---|---|
| `base` | System update, `python3-picamera2`, camera tools, `git`, `htop`, `ffmpeg` | all days |
| `litert` | `~/tflite_env`: `numpy`, `pillow`, `matplotlib`, `opencv-python`, `ai-edge-litert`, `onnx`, `onnxruntime`, Jupyter | Days 7 and 9 |
| `yolo` | `~/yolo`: `torch`, `torchvision`, `ultralytics` 8.4.171, `ncnn`, `ai-edge-litert`, `paho-mqtt`, `psutil`, `prometheus-client`, `flask`, Jupyter | Days 8, 11, 13 |
| `slm` | Ollama, and `~/ollama`: `ollama`, `requests`, `pydantic`, Jupyter | Day 10 |
| `network` | `iperf3`, `mosquitto`, `mosquitto-clients`, `avahi-utils` | Days 11 to 13 |

To install one part only, name it: `bash ~/HW-04/setup_pi.sh yolo`.

### 4. Add the other preparations

Do these steps on the master card before the copy:

| Folder | Content |
|---|---|
| `HW-05` | Download the language models |
| `HW-06` | Install MediaMTX |
| `HW-07` | Set the Mosquitto broker for the lab network |
| `HW-08` | Install Prometheus and Grafana |

### 5. Check the master

```bash
bash ~/HW-04/check_pi.sh
```

All lines must show `PASS`. The last line is `RESULT: PASS`.

To use an environment:

```bash
source ~/yolo/bin/activate
```

To start Jupyter for a laptop in the same network (from the book):

```bash
jupyter lab --ip=0.0.0.0 --no-browser
```

Open the address that the command prints. Replace the host with
`pi-NN.local`.

### 6. Copy the master card

1. On the master:

   ```bash
   bash ~/HW-04/prepare_master.sh
   ```

   The Raspberry Pi shuts down. Wait until the green LED is off.

2. Put the master card in the card reader of a Linux laptop. Find its device
   name with `lsblk`. In the commands below, `/dev/sdX` is that device.

   **A wrong device name destroys the data of that device.** Compare the size
   in `lsblk` with the size of the card.

3. Read the card into an image file:

   ```bash
   sudo dd if=/dev/sdX of=edgeai-master.img bs=4M status=progress conv=fsync
   ```

4. Optional: make the image smaller with PiShrink
   (`github.com/Drewsif/PiShrink`). A small image is faster to write. It also
   fits on a card that is some megabytes smaller than the master card. The
   system grows to the full card at the first start.

   ```bash
   sudo pishrink.sh edgeai-master.img
   ```

5. Write the image to each card. Use Raspberry Pi Imager: select
   `Use custom`, select `edgeai-master.img`, and select no change of the
   settings. Or use `dd`:

   ```bash
   sudo dd if=edgeai-master.img of=/dev/sdX bs=4M status=progress conv=fsync
   ```

On macOS and Windows, Raspberry Pi Imager writes the image. To read the
master card, use a Linux computer, or the Raspberry Pi itself with a USB card
reader.

### 7. Give each copy its identity

Start **one** copy at a time. All copies have the name `pi-00` before this
step, so two new copies in the network have the same name.

```bash
ssh edge@pi-00.local
sudo bash ~/HW-04/set_hostname.sh 07
```

The Raspberry Pi starts again with the name `pi-07`. Put a label with the
group number on the board and on the card.

The laptop can refuse the connection, because the key of `pi-00.local`
changed. Remove the old key first:

```bash
ssh-keygen -R pi-00.local
```

### 8. Shut down

Always shut down before you remove the power (from the book):

```bash
sudo shutdown -h now
```

Wait until the green LED is off.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `setup_pi.sh` | new | Commands from the sources above | not tested on a Raspberry Pi |
| `check_pi.sh` | new | Camera and temperature commands from the book | Tested on the work computer (x86, no camera): the script runs to the end and reports the missing parts as FAIL. Not tested on a Raspberry Pi. |
| `prepare_master.sh` | new | no source | not tested |
| `set_hostname.sh` | new | no source | The checks of the arguments were tested. The changes of the system were not tested. |

Open points for the test:

- The sources were written for the release "Bookworm" (Python 3.11). The
  current release of Raspberry Pi OS can be newer. A package can need a
  different version.
- `ai-edge-litert`, `torch`, and `ultralytics` must have a wheel for the
  Python version of the operating system.
- `pip` can install a NumPy version in an environment that is different from
  the system version. `picamera2` then can fail in that environment.
  `check_pi.sh` tests the import of `picamera2` in each environment.

## Test steps for the instructor

- Date of the test:
- Release of Raspberry Pi OS (`cat /etc/os-release`):
- Python version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run steps 1 and 2 | Time for the first start. Does `pi-00.local` work on the lab router? | |
| 2 | Run step 3 | Total time of `setup_pi.sh`. Errors in `~/setup_pi.log`. | |
| 3 | `df -h ~` after the setup | Used space of the card | |
| 4 | Run step 5 | Each FAIL line. The camera name that the script prints. | |
| 5 | In each environment: `python -c "import numpy; print(numpy.__version__)"` | The three NumPy versions and the system version | |
| 6 | `~/yolo/bin/pip freeze`, and the same for the two other environments | The versions for `Labs/VERSIONS.md` | |
| 7 | Run step 6 | Size of the image, time to read, time to write one card | |
| 8 | Run step 7 on two copies | Do both copies get different IP addresses? Does `ssh edge@pi-NN.local` work? | |
| 9 | Run `check_pi.sh` on one copy | RESULT line | |
| 10 | `vcgencmd measure_temp` at rest and after 5 minutes of `stress` or of a YOLO loop | Both temperatures, with the active cooler | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the release of the operating system and the package versions in
   `Labs/VERSIONS.md`.
3. If a package needs a fixed version, write the version in `setup_pi.sh`.
4. Keep the file `edgeai-master.img`. A broken card then needs only step 6.5
   and step 7.

## Credits

The steps adapt the Raspberry Pi setup chapter of "Machine Learning Systems"
by Vijay Janapa Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0), and
the setup steps of "Edge AI Engineering: Raspberry Pi" by Marcelo Rovai
(mjrovai.github.io/EdgeML_Made_Ease_ebook) and of "EdgeML with Raspberry Pi"
(github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0).
