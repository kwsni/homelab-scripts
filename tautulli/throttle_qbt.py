#!/usr/bin/env python
'''
Throttles qBittorrent traffic while Plex detects active playback

Required python modules: requests

Tautulli triggers: Playback start, Playback resume, Playback stop, Playback pause
Arguments:
    Playback start: start {streams}
    Playback resume: start {streams}
    Playback stop: stop {streams}
    Playback pause: stop {streams}
'''
import sys, requests

# Change these to match your configuration
QBIT_HOSTNAME = 'http://localhost:8080'
QBIT_USER = 'admin'
QBIT_PASS = 'adminadmin'

def main():
    try:
        trigger = sys.argv[1]
        streams = int(sys.argv[2])
    except:
        print('Invalid argument')
        return
    
    # authenticate to qBittorrent WebUI API
    url = f'{QBIT_HOSTNAME}/api/v2/auth/login'
    headers = {'Referer': QBIT_HOSTNAME}
    auth = {'username': QBIT_USER, 'password': QBIT_PASS}

    login = requests.post(url, headers=headers, data=auth, verify=False)

    if(login.status_code == 200 and login.cookies):
        # check toggle state
        url = f'{QBIT_HOSTNAME}/api/v2/transfer/speedLimitsMode'

        state = requests.get(url, cookies=login.cookies, verify=False)
        is_throttled = bool(int(state.content))

        # toggle throttle off
        if(is_throttled and streams < 1 and trigger == 'stop'):

            url = f'{QBIT_HOSTNAME}/api/v2/transfer/toggleSpeedLimitsMode'

            requests.post(url, cookies=login.cookies, verify=False)

        # toggle throttle on
        elif(not is_throttled and trigger == 'start'):

            url = f'{QBIT_HOSTNAME}/api/v2/transfer/toggleSpeedLimitsMode'

            requests.post(url, cookies=login.cookies, verify=False)

        # logout and end session
            
        url = f'{QBIT_HOSTNAME}/api/v2/auth/logout'

        requests.post(url, cookies=login.cookies, verify=False)
    else:
        print('Login failed')
        return

if __name__ == '__main__':
    main()