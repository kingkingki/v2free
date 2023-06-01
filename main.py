import requests
import json
import os

requests.packages.urllib3.disable_warnings()
SCKEY = os.environ.get('SCKEY')
TG_BOT_TOKEN = os.environ.get('TGBOT')
TG_USER_ID = os.environ.get('TGUSERID')


def checkin(email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'),
            base_url=os.environ.get('BASE_URL'), ):
    email = email.split('@')
    email = email[0] + '%40' + email[1]
    session = requests.session()
    session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='

    post_data = post_data.encode()

    response = session.post(login_url, post_data, headers=headers, verify=False)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
            
    response = json.loads(response.text)
    print(response['msg'])
    return response['msg']


result = checkin()


# post message by feishu robot
url = 'https://open.feishu.cn/open-apis/bot/v2/hook/02c2f817-ed14-45db-8681-8b9bb8cd6216'
headers = {'Content-Type': 'application/json'}
data = {
  "msg_type": "text",
  "content": {
    "text": result
  }
}
response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    print("飞书机器人消息发送成功")
else:
    print("飞书机器人消息发送失败")


# post message by feishu robot
url = 'https://open.feishu.cn/open-apis/bot/v2/hook/7fe750a8-a325-4839-bae7-432f985c04e5'
headers = {'Content-Type': 'application/json'}
data = {
  "msg_type": "text",
  "content": {
    "text": result
  }
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    print("飞书机器人消息发送成功")
else:
    print("飞书机器人消息发送失败")


if SCKEY != '':
    sendurl = 'https://sctapi.ftqq.com/' + SCKEY + '.send?title=v2free机场签到&desp=' + result
    r = requests.get(url=sendurl)
if TG_USER_ID != '':
    sendurl = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_USER_ID}&text={result}&disable_web_page_preview=True'
    r = requests.get(url=sendurl)
