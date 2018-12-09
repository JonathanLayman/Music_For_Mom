from gmusicapi import Mobileclient
import os
import errno
print("Import Successful")

mm = Mobileclient()
filename = os.getcwd() + '\oauth\oauth_code.txt'
print(filename)
# Create blank file
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(filename, "w") as f:
    f.write("")

mm.perform_oauth(storage_filepath=filename)

print("load successful")


def get_android_id(client):
    devices = client.get_registered_devices()
    android_device = None
    for device in devices:
        if device["type"] == "ANDROID":
            android_device = device["id"][2:]
            break
    else:
        print("There are no android devices for this account")
        quit()

    print(android_device)
    with open("oauth/device_id.txt", "w") as f:
        f.write(android_device)


mm.oauth_login(mm.FROM_MAC_ADDRESS, 'oauth/oauth_code.txt')

get_android_id(mm)
