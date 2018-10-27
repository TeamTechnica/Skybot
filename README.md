## Connecting to Twilio

We used Twilio’s Programmable SMS to set this up as an SMS service. Specifically, we wrote a function that will communicate with the Twilio API to provide a response, `sms_reply()`. For this function we use the `route()` decorator to tell Flask which URL should trigger this function.

``` python
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
``` 


This function is triggered whenever a message is sent to our Twilio number. With `requests.values.get`, we retrieve several attributes associated with the message received from a user, including their phone number. To indicate this, we made the first parameter `From`; this yields a result in the format “+1XXXXXXXXXX.”

``` python 
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('From', None)
```

