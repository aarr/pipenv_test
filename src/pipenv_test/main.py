import requests

def get_ip():
    response = requests.get('https://httpbin.org/ip')
    ip = response.json()['origin']
    print('Your IP is {0}'.format(ip))
    return ip

if __name__ == '__main__':
    get_ip()