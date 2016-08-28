import requests
import datetime
import json

# Setup
l = "Concord, NH"

def get_sun_data(t, l, tz):
    url = "http://api.usno.navy.mil/rstt/oneday?date={}/{}/{}&loc={}&tz={}".format(t.month, t.day, t.year, l, tz)
    req = requests.get(url)
    json_data = req.text
    data = json.loads(json_data)
    sundata = data['sundata']
    return sundata

def lambda_handler(event, context):

    intent=event['request']['intent']
    print "Intent = {}".format(intent)

    slots = intent['slots']
    slot = slots['MyCity']
    value = slot['value'] #will be: sunlite concord nh
    city = value[0:-3]
    state = value[-2:]

    t = datetime.date.today()
    # loc = "Concord, NH"
    loc = "{},{}".format(city, state)

    sun_data = get_sun_data(t, loc, -5)
    print sun_data
    sunset = sun_data[3]['time'][0:-2]
    dusk = sun_data[4]['time'][0:-2]
    dawn = sun_data[0]['time'][0:-2]
    sunrise = sun_data[1]['time'][0:-2]

    message = "For the City {} ".format(loc)
    message += "Sunset is at {} .".format(sunset)
    message += "Dusk ends at {} .".format(dusk)
    message += "Dawn breaks at {} ".format(dawn)
    message += "and the sun rises at {} .".format(sunrise)

    print "Message = {}".format(message)

    response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': message,
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + 'Sunlite',
            'content': 'SessionSpeechlet - ' + message,
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Reprompt',
            }
        },
        'shouldEndSession': True
    }

    return {
        'version': '1.0',
        'response': response
    }

if __name__ == "__main__":
    lambda_handler(1,1)
