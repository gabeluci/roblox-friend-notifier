# Roblox Friend Notifier

This Python script (checkrobloxfriends.py) will send you an email when one of your Roblox friends are online.
It will send you a new email each time a friend logs on or off.

There are a couple ways you can run this. You can run it on your own computer (like as a scheduled task in Windows) or you can run it in GitHub Actions. Instructions below.

## Scheduled Task in Windows
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
# ======== UNLESS YOU'RE USING GITHUB ACTIONS ============

# Get this cookie value from your browser after logging in.
# If you don't know how, see this: https://devforum.roblox.com/t/how-to-use-the-roblox-web-api-endpoints/1829973#how-to-get-roblox-security-cookie-5
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


## GitHub Actions

This can be run by GitHub Actions, and triggered by cron-job.org (or anything else that can call a URL on a schedule).

1. Fork this repository
2. In your forked repository, click "Settings" at the top
3. On the left, click "Secrets and variables", then "Actions"
3. Under "Repository secrets", set all of the following variables. See above for how to get these values.
    ```
    ROBLOX_COOKIE
    ROBLOX_USER_ID
    SMTP_FROM_ADDRESS
    SMTP_PASSWORD
    SMTP_PORT
    SMTP_SERVER
    SMTP_TO_ADDRESS
    SMTP_USERNAME
    ```

At this point, the action should work. Test it on the actions workflow page:

1. Click "Actions" at the top
2. Click "Check my friends" on the left
3. Click the "Run workflow" button on the right, then the green "Run workflow" button. Make sure it works.

Now you need to schedule it to run automatically. GitHub Actions does have a feature to schedule runs, but it isn't reliable. If you tell it to run every 15 minutes, it'll run every couple hours... maybe. But you can trigger the workflow reliably by calling a URL. You need to create a GitHub access token first.

1. On the [Fine-grained personal access tokens](https://github.com/settings/personal-access-tokens) page, click "Generate new token"
2. Set these values:
    - Token name: "Run roblox-friend-notifier workflows"
    - Expiration: Whatever you want. If you chose an expiration, you'll need to update it when it expires.
    - Repository access: Select "Only select repositories"
        - "Select repositories" and select "roblox-friend-notifier"
    - Under "Permissions"
        - Add permissions: Select "Actions"
        - Beside "Actions" in the list change "Access" from "Read-only" to "Read and write"
    - Click "Generate token"
    - Copy the token and paste it anywhere (like Notepad) temporarily. This is the only time you'll see it.

Now the workflow can be triggered by an HTTP call using that token to authenticate. I set this up with [cron-job.org](https://cron-job.org). If you'd like to do this, create an account and login, then:

1. Click "CREATE CRONJOB" in the top right
2. Set these values:
    - Title: "Roblox Friend Notifier"
    - URL: `https://api.github.com/repos/[username]/roblox-friend-notifier/actions/workflows/scheduled_run.yml/dispatches`
        - Replace "[username]" with your username
    - Set the "Execution Schedule" to whatever you want
3. Click "Advanced"
4. Under "Headers", add these values:
    - Key: `X-GitHub-Api-Version`

      Value: `2026-03-10`
    
    - Key: `Content-Type`

      Value: `application/vnd.github+json`

    - Key: `Authorization`

      Value: `Bearer token` (replace "token" with the GitHub token you created earlier)
5. Under "Advanced", set these values:
    - Request method: `POST`
    - Request body: `{"ref":"main"}`
6. Click "TEST RUN" at the bottom to make sure it works, then "SAVE"
7. ?
8. Profit