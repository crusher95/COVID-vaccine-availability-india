import urllib3
from datetime import datetime, timedelta
import json
from pprint import pprint

#02-05-2021
current_date = datetime.now()
date_format = "%d-%m-%Y"


whatsapp_update_number = "https://api.callmebot.com/whatsapp.php?phone={}&text={}&apikey={}"

http = urllib3.PoolManager()

with open("config.json") as f:
	notify_to = json.load(f)

for user in notify_to.keys():
	#checks for next 6 weeks
	result = {'45+': {}, '18+': {}}
	for district in notify_to[user]['districts']:
		for week in range(0, 42, 7):
			ref_date = current_date + timedelta(days=week)
			url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district, ref_date.strftime(date_format))

			r = http.request('GET', url)
			for center in json.loads(r.data)['centers']:
				try:
					for session in center['sessions']:
						if session['available_capacity'] > 0:
							if session['min_age_limit'] >=45:
								key_name = '45+'
							elif session['min_age_limit'] >= 18:
								key_name = '18+'
							if center['name'] not in result[key_name]:
								result[key_name][center['name']] = {'available_capacity': 0, 'dates': [], 'vaccine': session['vaccine'], 'fee_type': center['fee_type']}
							result[key_name][center['name']]['available_capacity'] += session['available_capacity']
							result[key_name][center['name']]['dates'].append(session['date'])

				except Exception as e:
					pprint(center)

	message = "Vaccine availability status for 18 and above in your district: {}"
	availabile_18 = ""

	for slot in result['18+'].keys():
		availabile_18 += slot + "({}) - {}, ".format(result['18+'][slot]['available_capacity'], result['18+'][slot]['dates'][0])


	if availabile_18!="":
		message = message.format(availabile_18)
		r = http.request('GET', whatsapp_update_number.format(user, message, notify_to[user]['api_key']))
		pprint("Available")
		pprint(user)
	else:
		pprint("Not Available")