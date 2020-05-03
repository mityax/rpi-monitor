# rpi-monitor
This simple script monitors the cpu temperature, core voltage and total voltage of a Raspberry Pi and their averages in realtime.

No setup is needed, just download the file and execute it like this:
```
$ python monitor.py
```

The first time you start it, it will prompt you if it should automatically create an alias in .bashrc so you
can launch it by only typing
```
$ monitor
```
the next time.

![Screenshot](https://raw.githubusercontent.com/mityax/rpi-monitor/master/Screenshot.png)

**Note:** The script should work on most linux systems with python installed (it's usually installed by default).
The .bashrc alias only works on systems using the bash as default shell. If your system doesn't (as for example LibreElec), you can create a bash alias manually. Just do a quick google search on how to do it.
