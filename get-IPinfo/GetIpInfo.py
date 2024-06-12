import requests


class LocationResolver:
    def __init__(self, amap_api_key, ipinfo_api_key):
        self.amap_api_key = amap_api_key
        self.ipinfo_api_key = ipinfo_api_key

    def get_ip_info(self, ip):
        # 使用ipinfo的API服务
        url = f"https://ipinfo.io/{ip}/json?token={self.ipinfo_api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to get IP info. Status code: {response.status_code}")
            return None

    def get_location_info(self, lat, lon):
        # 使用高德地图逆地理编码服务获取详细地址信息
        url = f"https://restapi.amap.com/v3/geocode/regeo?location={lon},{lat}&key={self.amap_api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1':
                location_name = data['regeocode']['formatted_address']
                address_component = data['regeocode']['addressComponent']
                # country = data['regeocode']['addressComponent']['country']
                # province = data['regeocode']['addressComponent']['province']
                # city = data['regeocode']['addressComponent']['city']
                # district = data['regeocode']['addressComponent']['district']
                # township = data['regeocode']['addressComponent']['township']
                # street = data['regeocode']['addressComponent']['streetNumber']['street']
                # number = data['regeocode']['addressComponent']['streetNumber']['number']
                # location = str(country)+str(province)+str(city)+str(district)+str(township)+str(street)+str(number)

                country = address_component.get('country', '')
                province = address_component.get('province', '')
                city = address_component.get('city', '')
                district = address_component.get('district', '')
                township = address_component.get('township', '')
                street = address_component.get('streetNumber', {}).get('street', '')
                number = address_component.get('streetNumber', {}).get('number', '')

                # location = f"{country}{province}{city}{district}{township}{street}{number}"
                location_parts = [country, province, city, district, township, street, number]
                location = ''.join(part for part in location_parts if part)

                return data, location, location_name
            else:
                return "No address found"
        else:
            print(f"Failed to get location info. Status code: {response.status_code}")
            return None


amap_api_key = '77726981d97090b4d515fcd7a1a38390'
ipinfo_api_key = '56c4c77d9ac6e4'

resolver = LocationResolver(amap_api_key, ipinfo_api_key)
ip_address = "103.151.149.5"
ip_info = resolver.get_ip_info(ip_address)

if ip_info:
    # print(f"IP: {ip_address}")
    # print(f"City: {ip_info.get('city')}")
    # print(f"Region: {ip_info.get('region')}")
    # print(f"Country: {ip_info.get('country')}")
    # print(f"Location: {ip_info.get('loc')}")
    # print(f"ISP: {ip_info.get('org')}")
    print(f"IP: {ip_address}")
    print(f"City: {ip_info.get('city', '')}")
    print(f"Region: {ip_info.get('region', '')}")
    print(f"Country: {ip_info.get('country', '')}")
    print(f"Location: {ip_info.get('loc', '')}")
    print(f"ISP: {ip_info.get('org', '')}")

    loc = ip_info.get('loc')
    if loc:
        lat, lon = loc.split(',')
        # print(lat,lon)
        detailed_address = resolver.get_location_info(lat, lon)
        # country = detailed_address['regeocode']['formatted_address']
        # print(country)
        if detailed_address[0]:
            print(f"All Address Info: {detailed_address[0]}")
            print(f"Detailed Location: {detailed_address[1]}")
            print(f"Address Name: {detailed_address[2]}")
else:
    print("Could not retrieve IP information.")
