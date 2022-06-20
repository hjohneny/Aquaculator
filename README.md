Hendrix
hjohneny99@gmail.com

Instructions

```bash
  cd Aquaculator
```

Install Libraries

```bash
  pip install requirements.txt
```

Start the server

```bash
  pyhton app.py
```

 Additional

1.	Unzip folder “Aquaculator”
2. 	Open powershell or run terminal in admin
3.	cd to unzipped folder (%directory%/Aquaculator/) and install Libraries with python command (make sure python is installed):
$ pip install requirements.txt
4.	Open .bat script below in a text editor
5.  Edit line 3 and change to your extracted file directory (e.g C:)
6.  Edit line 4 to cd <..\your\unzipped\directory\..> (e.g. C:/downloads/Aquaculator)
7.	Execute Run.bat script in the file.


shell script below. copy paste and save as .bat extension
-------------------------------------------------
@echo on

%Disk%:
cd %AquaculatorDirectory%
start http://localhost:5000/
python app.py

cmd /k

