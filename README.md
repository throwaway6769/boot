full setup
```
sudo apt install git
cd /var
sudo mkdir esp32
cd esp32
sudo git clone https://github.com/throwaway6769/boot
cd boot
```
view file in terminal
```
cd /var/esp32/boot
cd folder
ls
cat filename.py
# or xdg-open filename.py
```
at the end of lab
```
sudo rm -rf /var/esp32/boot
sudo rm ~/.bash_history
history -c && history -w
exit
```
