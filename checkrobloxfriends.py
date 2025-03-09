import sys,requests,smtplib,pickle,os.path
from email.message import EmailMessage

# =============== CHANGE THESE SETTINGS ==================

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


def send_email(subject, message):
    try:

        if smtp_username is None or smtp_password is None:
            # no email address or password
            # something is not configured properly
            print("Did you set email address and password correctly?")
            return False

        # create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        msg.set_content(message)

        # send email
        with smtplib.SMTP_SSL(smtp_server, smpt_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Problem during sending email")
        print(repr(e))
    return False

class Result(object):
	status_code = 200
	data = []

if os.path.exists(pickle_file):
	with open(pickle_file,"rb") as fi:
		last_result = pickle.load(fi)
else:
	last_result = Result()

r = requests.get("https://friends.roblox.com/v1/users/" + str(roblox_userid) + "/friends/online", cookies=roblox_cookie)

new_result = Result()
new_result.status_code = r.status_code

print("Roblox status code: " + str(r.status_code))

if r.status_code == 401 and last_result.status_code != 401:
	send_email("Roblox notifier error","Needs new cookie")
elif r.status_code == 200:
	data = r.json()["data"]
	new_result.data = data
	online = []
	for user in data:
		online.append(user["id"])
	wasonline = []
	for user in last_result.data:
		wasonline.append(user["id"])
	online.sort()
	wasonline.sort()
	if online != wasonline:
		if online:
			# We only have the friends' ID's, so now we go get their names
                        idrequestdata = {}
                        idrequestdata["userIds"] = online
                        idrequestdata["excludeBannedUsers"] = True
                        fr = requests.post("https://users.roblox.com/v1/users", json=idrequestdata, cookies=roblox_cookie)
			onlinefriends = []
			if fr.status_code == 200:
				friends = fr.json()["data"]
				for friend in friends:
					if next((id for id in online if id == friend["id"]), None) != None:
						onlinefriends.append(friend["name"])
					if len(onlinefriends) == len(online):
						break
			else:
				# If we couldn't get the list of friends for whatever reason, just use the id's
				onlinefriends = online
			
			print(onlinefriends)
			send_email("Roblox notifier", " is online\n".join(onlinefriends) + " is online")
		else:
			send_email("Roblox notifier", "No one is online anymore")
elif r.status_code != 429:
	send_email("Roblox notifier error", "Status code: " + str(r.status_code) + "\nData:\n\n" + str(r.json()))

with open(pickle_file, "wb") as fi:
	pickle.dump(new_result, fi)

