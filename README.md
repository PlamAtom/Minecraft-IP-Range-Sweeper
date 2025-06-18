## 🖥️ Compatibility

This software was developed based on Python 3.11 on the Windows operating system. (Python is required to run)

## 🚀 Installation

### ✅ 1. Install Python 3.11
You can download it from:

👉 https://www.python.org/downloads/release/python-3110/

*You can also try running it with the version of Python you might already have installed.*

---

### 📥 2. Download or Clone This Repository

You can either:

- 1- [Download the ZIP](https://github.com/PlamAtom/Minecraft-IP-Range-Sweeper/archive/refs/heads/main.zip) manually from GitHub,  
**or**
- 2- Use [Git](https://git-scm.com/downloads) to clone the repository:

After installing Git, create a folder and a .cmd file (for example, get-repo.cmd) with the following line, then run it:

    git clone https://github.com/PlamAtom/Minecraft-IP-Range-Sweeper.git

## 📖 Windows Tutorial

Follow these steps to start scanning and find potential Minecraft server IPs:

▶️ 1. Run the Scanner

Double-click windows_start.bat to launch the tool.
![]([https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png](https://ibb.co/GfJ7BSWY))

✅ 2. Accept Disclaimer

You'll be shown a disclaimer. Type I Understand to continue.

🌍 3. Enter the IP Prefix

Input the first two sections of the IP address you expect to find.

Example: If the server IP was 81.243.192.182:25565, you enter 81.243

🔢 4. Enter the Port Number

Provide the last known port used by the server. This might be different from the default 25565 depending on how the server is configured.

🎯 5. Define the IP Range

Set the IP range using a dash (-).
It is highly recommended to enter 0-255 which is the upper-limit

You can narrow the range depending if you have good educated guesses

🛠️ 6. Start Scanning

Confirm by typing Y when prompted to run the scanner.

⚙️ 7. Set the Number of Scanners

Input how many scanner instances to run.
Note: Each value spawns about twice as many due to delay.

Example: Typing 10 runs ~20 tasks at once. I usually run 30-35 for a fast scan. 
Avoid too high numbers for your system as it may cause system instability.

⏳ 8. Wait for Completion

The scanning windows will automatically close once it finishes.

📂 9. View Results

Run windows_results.bat and open the generated results.txt file.

Filename should something like: results_2025-06-18_03-30-17.txt

🎮 10. Try the IPs in Minecraft

Test the listed IP addresses manually in Minecraft until you find the right one.
Since this targets typical consumer ISP ranges, the list should be relatively short and easy to try out.
