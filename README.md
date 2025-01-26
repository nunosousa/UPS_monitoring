# UPS data log analysis
This repository contains a set of scripts created to help me analysis the stability of the electrical power that feeds my home.

I have a generic UPS from which data is retrieved trough the available USP connection.

The data link is managed with the Network UPS Tools (NUT) and the data is analyzed in python.

## Notes on setting up Network UPS Tools

First install NUT:
```
apt install nut

```

Configure the file /etc/nut/nut.conf with:
```
MODE=standalone
```

Append the following entry to the file /etc/nut/ups.conf:
```
[EuroTech]
    driver = nutdrv_qx
    desc = "EuroTech 640VA UPS"
    port = "auto"
    vendorid = 0001
    productid = 0000
    bus = 001
    novendor
    norating
    noscanlangid
    protocol = hunnox
    langid_fix = "0x0409"

```
Note: Info retrieved from https://networkupstools.org/ddl/Powercool/650VA.html.

Check if some changes are required to /etc/nut/upsmon.conf and /etc/nut/upsd.conf.

Run the following commands to start the NUT server and peek the UPS's current values:
```
sudo systemctl enable --now nut-server

sudo systemctl restart --now nut-monitor

upsc EuroTech@localhost
```

If everything is configured properly, run the following command log the selected UPS parameters to a file:
```
upslog -s EuroTech@localhost -i 1 -l /home/nunosousa/upslog.txt
upslog -s EuroTech@localhost -f "%ETIME% %TIME @Y@m@d @H@M@S% %VAR battery.voltage% %VAR input.frequency% %VAR input.voltage% %VAR input.voltage.fault% %VAR output.voltage% %VAR ups.load% %% %VAR ups.status% %% %VAR ups.temperature%" -i 1 -l /home/nunosousa/upslog.txt
```

## Notes on setting up the Python virtual environment

### Creating a virtual environment
To create a virtual environment, run venv.
```
python3 -m venv .venv
```

### Activating a virtual environment
```
source .venv/bin/activate
```

### Ensure pip, setuptools, and wheel are up to date
```
python3 -m pip install --upgrade pip setuptools wheel
```

### Installing packages using requirements file
```
python3 -m pip install -r requirements.txt
```

### Starting JupyterLab
Start JupyterLab using:
```
jupyter lab
```

### Leaving the virtual environment
If you want to switch projects or otherwise leave your virtual environment, simply run:
```
deactivate
```
### Update project dependencies
If new dependencies where installed, run:
```
python3 -m pip freeze > requirements.txt
```

Check all installed packages with:
```
python3 -m pip list
```
