import requests

def get_atmospheric_conditions(username, password, lat=12.9716, lon=77.5946):
    """Fetches real-time weather telemetry from Meteomatics API using 'now'."""
    url = f"https://api.meteomatics.com/now/t_2m:C,relative_humidity_2m:p,wind_speed_10m:ms/{lat},{lon}/json"
    try:
        response = requests.get(url, auth=(username, password), timeout=10)
        if response.status_code == 200:
            data = response.json()
            parameters = data.get("data", [])
            result = {}
            for param in parameters:
                param_name = param.get("parameter")
                values = param.get("coordinates", [])[0].get("dates", [])[0].get("value")
                result[param_name] = values
            return result
        else:
            return None
    except Exception:
        return None
