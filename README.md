# Roblox Friend Notifier

This Python script (checkrobloxfriends.py) will send you an email when one of your Roblox friends are online.
It will send you a new email each time a friend logs on or off.


## Installation
On Windows, install Python from the [Microsoft Store](https://apps.microsoft.com/detail/9NCVDN91XZQP) or download from the [Python website](https://www.python.org/downloads/). If you're running Linux, then you already know what to do.

Then install the prerequisite modules. From a terminal:

```
pip install requests
```

Then set it up to run every 15 minutes, or whatever interval you like. On Windows, you can use Task Scheduler. I've included a ready-made task you can import.

1. Download `Roblox Friend Notifier Task.xml`
2. Open it in a text editor and modify the `<WorkingDirectory>` value at the bottom of the file to the location where you put `checkrobloxfriends.py`
3. Open Task Scheduler (Start menu and type "task scheduler").
4. Right-click "Task Scheduler Library".
5. Click "Import Task" then choose `Roblox Friend Notifier Task.xml`
6. Change any settings you want

For it to work you will need to change the settings at the top of the file:

```py
# =============== CHANGE THESE SETTINGS ==================

# Get this cookie value from your browser after logging in. If you don't know how, see this:
# https://devforum.roblox.com/t/how-to-use-the-roblox-web-api-endpoints/1829973#how-to-get-roblox-security-cookie-5
# You'll get an email when this cookie expires. When that happens, get a new one.
# To make it last longer, delete the cookie from the browser once you copy it so that only
# this script is using this cookie.
roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS....."}

# Your user ID number can be found by going to your profile page.
# The number is in the URL.
roblox_userid = 123

# Email credentials
# If you're using GMail, you'll need to generate an app password: https://support.google.com/accounts/answer/185833
smtp_server = "smtp.gmail.com"
smpt_port = 465
smtp_username = "youremail"
smtp_password = "password"

# The SMTP username is usually an email address, so we'll use it
# as the From and To addresses in the email. If you don't want that
# then change these.
from_address = smtp_username
to_address = smtp_username

# This is a file where the results are saved so that we can compare it to
# the next time this runs. The default will save it in the same
# folder where this script is, which means the user account used to
# run this script needs write permissions to that folder.
pickle_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkrobloxfriends.pk")

# =============== END OF SETTINGS ==================
```
