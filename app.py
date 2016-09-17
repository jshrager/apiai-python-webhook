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
    elif req.get("result").get("action") == "liked_product":
        res = makeWebhookResult({ "response_type": "liked_product" })
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

        if data.get("style") == "modern":
            facebook_message = {
                "quick_replies":[
                    {
                        "content_type":"text",
                        "title":"I don't like these",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                        "image_url":"http://media.syracuse.com/news/photo/2013/12/13953661-standard.jpg"
                    }
                ],
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Alonso Bathroom Suite",
                                "image_url": "http://st.hzcdn.com/simgs/bc21031e03b3c4f5_8-4182/contemporary-bathroom.jpg",
                                "subtitle": "Lovely contemporary bathroom suite.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/14206890/alonso-bathroom-suite-contemporary-bathroom-other-metro",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
                                    }
                                ]
                            },
                            {
                                "title": "Classic White Bathroom",
                                "image_url": "http://st.hzcdn.com/simgs/bd61dcc607117cc4_8-4600/modern-bathroom.jpg",
                                "subtitle": "Photo of a small contemporary white bathroom.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/52981573/mesa-bathroom-modern-bathroom-other-metro",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
                                    }
                                ]
                            },
                            {
                                "title": "Wood Effect",
                                "image_url": "http://st.hzcdn.com/simgs/24b1cd8b06b468e4_8-3914/contemporary-bathroom.jpg",
                                "subtitle": "Ultra modern wood effect tiles.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/47950727/queens-gate-mews-contemporary-bathroom-london",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        elif data.get("style") == "traditional":
            facebook_message = {
                "quick_replies":[
                    {
                        "content_type":"text",
                        "title":"I don't like these",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                        "image_url":"http://media.syracuse.com/news/photo/2013/12/13953661-standard.jpg"
                    }
                ],
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "White Tiled Bathroom",
                                "image_url": "http://st.hzcdn.com/simgs/4301648c0374c290_8-9828/traditional-bathroom.jpg",
                                "subtitle": "Traditional bath and shower.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/12276216/bathroom-remodeling-traditional-bathroom-south-east",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
                                    }
                                ]
                            },
                            {
                                "title": "Traditional London Bathroom",
                                "image_url": "http://st.hzcdn.com/simgs/3ef15947075192a4_8-3755/traditional-bathroom.jpg",
                                "subtitle": "Exposed shower valves.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/56172600/walthamstow-london-traditional-bathroom-london",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
                                    }
                                ]
                            },
                            {
                                "title": "Country with a touch of chic",
                                "image_url": "http://st.hzcdn.com/simgs/72112c6107d9b81f_8-7685/traditional-cloakroom.jpg",
                                "subtitle": "Victorian Basin.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://www.houzz.co.uk/photos/66744118/wimbledon-common-traditional-cloakroom-london",
                                        "title": "View More Details"
                                    },
                                    {
                                        "type": "postback",
                                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                                        "title": "I like"
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

    elif data.get("response_type") == "liked_product":

        print("liked")

        speech = "OK, opening the app now!"

        facebook_message = {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Awesome, just click one of the options below!",
                    "buttons":[
                        {
                        "type":"web_url",
                        "url":"https://petersapparel.parseapp.com",
                        "title":"Open App"
                        },
                        {
                        "type":"web_url",
                        "url":"https://petersapparel.parseapp.com",
                        "title":"Download App"
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
