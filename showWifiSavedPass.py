import re
import subprocess

command_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []
for name in profile_names:
	wifi_profile = dict()
	profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', name], capture_output=True).stdout.decode()
	if re.search("Security Key           : Absent", profile_info):
		continue
	else:
		wifi_profile['ssid'] = name
		profile_info_pass = subprocess.run(['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], capture_output=True).stdout.decode()
		password = re.search("Key Content            : (.*)", profile_info_pass)
		if password == None:
			wifi_profile['password'] = None
		else:
			wifi_profile['password'] = password[1]
	wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
	print(f"""{x+1}. {wifi_list[x]['ssid']} - 
	Password: {wifi_list[x]['password']}""")
	print()
print("Press Enter to exit")
input()