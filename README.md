# COVID-vaccine-availability-india
A service that sends you whatsapp alert in case there is vaccine available in your district.

# How to use
Rename the file `sample-config.json` to `config.json`

Update config.json:
```
{
	"+91887xxxxx48" <Replace with your mobile number>: {
		"districts": [650, 651] <Replace with the district numbers you want to track>,
		"api_key": "652314" <Replace with Callme bot API key>
	}
}
```

Call me bot API key: [Get API key](https://www.callmebot.com/blog/free-api-whatsapp-bot/) API key

Run the following command in your terminal:
`python3 cowin_slot_available.py`

