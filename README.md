# check mqtt connection via prometheus
This program designed to check mqtt connection and report via prometheus

By change the name config-sample.py to config.py and adding your config to config file <br> 
you can check your mqtt connection and receive messages by prometheus on defined port <br>

Here supposed that your mqtt is up by docker in same server witch this program is running <br>
and if your mqtt stops working this code will restart your docker file.

to run this app follow steps below: <br>
``` pip install requirements ``` <br>
``` python refMain.py```
