## TwistedProxy
**TwistedProxy** is a python proxy that aims to capture, decrypt & save Clash Royale game traffic. This is an adapted version for v2.3 that use a workaround based on frida since Supercell enforced their game protection which make the serverKey patching impossible.

### Setup the proxy
The proxy need some external dependencies to run:

1. Install **ADB** and add it to your path
2. Setup **frida-server** on your device, here is a guide: [https://www.frida.re/docs/android/](https://www.frida.re/docs/android/)
3. Push fake\_dev\_urandom file on your device (at /data/data/com.supercell.clashroyale)
4. Install the modded version of **tweetnacl**. Just run `python setup.py install` in TweetnaclMod directory to install it
5. Run `python -m pip install -r requirements.txt` to install the others dependencies

### How to use it ?

To start the proxy you will just have to run the following command:
> python Main.py

**Note**: You don't need to start the game, the proxy will do it itself.

However the proxy accept some optionals arguments that are:

* `-v`: if specified, the proxy will be run in verbose mode that basically output packets hexdump in terminal
* `-r`: if specified, all packets will be saved in the repository you've set in config.json (ReplayDirectory key).

### Credits

[Misha](https://github.com/MISHA-CRDEV) - For the crypto workaround and help with the frida script

### PS

Any question or bug to report ? Feel free to contact me at @GaLaXy1036#1601 on discord