# pontaje-sync-time-script
  This Basic Python Script can be usefull to syncronise time entries for zkteco devices to a laravel api.
  If your device is not recognised in local network (arp -a), first install zkteco software and add device manually, after adding,the device should be visible and respond to ping.

# usefull resource
 https://www.zkteco.com/en/ZKAccess_3/ZKAccess3.5

Make executable
import certifi
print(certifi.where())

pyinstaller --hidden-import=requests --hidden-import=zk --add-data "C:\Users\rb\Documents\pontaje-sync-time-script-master\certifi\cacert.pem;." fetchUsers.py
