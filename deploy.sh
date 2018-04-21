rm config.ini

name="/dev/"`(ls /dev/ | grep -G [s][d][^a][1])`
echo ${name}

sudo umount $name
sudo mount $name /home/josh/usb
sudo cp -rf * /home/josh/usb
sleep 1
sudo umount $name