import requests
import json

endpoint = 'https://free.currencyconverterapi.com/api/v5/convert?q=CNY_USD,USD_CNY&compact=y'

def send_error(key, message):
    print(json.dumps({"id": key, "message": message}))

def handle(r):
    """handle a request for conversion, hitting a free converter and returning the response.
    Args:
        req (str): request body
    """
    try:
        if r == "":
            req = {}
        else:
            req = json.loads(r)
    except json.decoder.JSONDecodeError:
        return send_error("unprocessable_entity", "the request body was malformed")

    to = req.get("to")
    if to not in ["RMB", "USD", "CNY"]:
        return send_error("unprocessable_entity", "invalid parameter to, must be RMB, CNY, or USD")
    if to == "RMB":
        to = "CNY"

    if to == "CNY":
        fro = "USD"
    else:
        fro = "CNY"

    count = req.get("ammount", req.get("count", 1))
    try:
        count = int(count)
        if count < 1:
            raise ValueError()
    except ValueError:
        return send_error("unprocessable_entity", "invalid parameter for ammount/count, must be positive integer")

    key = "%s_%s" % (fro, to)
    try:
        rate = requests.get(endpoint, timeout=5).json()[key]["val"]
    except requests.exceptions.Timeout:
        return send_error("service_unavailable", "timeout accessing service")
    except:
        return send_error("internal_error", "an error occurred")

    print(json.dumps({"rate": rate, "from_to": key, "value": rate * count}))

#if __name__ == "__main__":
#    handle('{"to":"USD", "count": "10"}')
