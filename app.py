#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "inspiration":
        res = makeWebhookResult({ "response_type": "inspiration", "style": req.get("result").get("parameters").get("style") })
    elif req.get("result").get("action") == "finding_products":
        res = makeWebhookResult({ "response_type": "finding_products" })
    else:
        return {}
    
    return res


def makeWebhookResult(data):
    print(data)
    if data.get("response_type") == "inspiration":

        speech = "Found some other stuff for you!"

        print(data)
        print("Response:")
        print(speech)

        facebook_message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Mesa Bathroom",
                            "image_url": "http://st.hzcdn.com/simgs/bd61dcc607117cc4_8-4600/modern-bathroom.jpg",
                            "subtitle": "Photo of a small contemporary ensuite bathroom.",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "http://www.houzz.co.uk/photos/52981573/mesa-bathroom-modern-bathroom-other-metro",
                                    "title": "View More Details"
                                },
                                {
                                    "type": "postback",
                                    "payload": "bathroom1",
                                    "title": "I Like This"
                                }
                            ]
                        }
                    ]
                }
            }
        }

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": facebook_message},
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

    elif data.get("response_type") == "finding_products":

        speech = "Found some other stuff for you!"

        facebook_message = {
            "text":"I've found some products you might be interested in.",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"Show Me",
                "payload":"Show Me"
              }
            ]
        }

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": facebook_message},
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

    else:
        speech = "Something went wrong!"

        return {
            "speech": speech,
            "displayText": speech,
            "data": "",
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
