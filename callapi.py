import requests
import os
class CallAPI:
    def callrailstats(self, source, caption, description, filepath):
        # 正常 normal / 欄杆異常 railbreak / 攝影機壞掉 cambreak
        
        url = os.getenv('APIURL', "http://220.132.208.73:5170/rail")
        # 按類型印出發報資訊
        if description == "normal":
            print("發報正常訊號")
        elif description == "railbreak":
            print("發報欄杆異常")
        elif description == "cambreak":
            print("發報攝影機異常")
        payload = {'source': source,
        'caption': caption,
        'description': description}
        headers = {}
        if filepath != "":
            files=[
            ('file',('helmet.jpg',open(filepath,'rb'),'image/jpeg'))
            ]
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
        else:
            response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        
        return response
