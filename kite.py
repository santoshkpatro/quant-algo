import os, time
from dotenv import load_dotenv
load_dotenv()
from kiteconnect import KiteConnect,KiteTicker
import urllib.parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import hmac, base64, struct, hashlib, time


zerodha_cred = {
    'User':{
        'user_id' : os.environ.get('KITE_USER_ID'),
        'password': os.environ.get('KITE_PASSWORD'),
        'api_key' : os.environ.get('KITE_API_KEY'),   
        'common_ans' : "",
        'api_secret' : os.environ.get('KITE_API_SECRET'),  
        'auth_key': os.environ.get('KITE_AUTH_KEY')
    },
}

print(zerodha_cred)

my_api_key=zerodha_cred['User']['api_key']

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    totp = str(get_hotp_token(secret, intervals_no=int(time.time())//30))
    if len(totp) < 6:
        totp = '0' + totp
    return totp


def getkite(_client):

    user_id = zerodha_cred[_client]['user_id']
    password = zerodha_cred[_client]['password']
    api_key = zerodha_cred[_client]['api_key']
    kite = KiteConnect(api_key=api_key)
    # common_ans = zerodha_cred[_client]['common_ans']
    auth_key = zerodha_cred[_client]['auth_key']
    url  = 'https://kite.trade/connect/login?v=3&api_key='+api_key 
    # telegram_bot_sendtext("Line 92")

    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disble-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        time.sleep(2)
        input_fields = driver.find_elements_by_tag_name('input')
        input_fields[0].send_keys(user_id)
        input_fields[1].send_keys(password)
        input_fields[1].send_keys(Keys.ENTER)
        time.sleep(1)
        two_fa = driver.find_elements_by_tag_name('input')
        common_ans = get_totp_token(auth_key)
        two_fa[0].send_keys(str(common_ans))
        two_fa[0].send_keys(Keys.ENTER)
        time.sleep(1)
        while("request_token=" not in driver.current_url):
            print (driver.current_url)
            driver.save_screenshot('login.png')
            time.sleep(3)
        redirect_url = driver.current_url
        #print('redirectURL-',redirect_url)
        parsed = urllib.parse.urlparse(redirect_url)
        query_dict = dict(urllib.parse.parse_qsl(parsed.query))
        request_token = query_dict['request_token']
        driver.close
        return request_token
    except Exception as e:
        print('closing')
        driver.close()

def gen_acc_token():
    users = ['User'] 
    auth_keys={}
    cur_date=datetime.now().strftime("%y_%m_%d")

    for _client in users:
        api_key = zerodha_cred[_client]['api_key']
        api_secret = zerodha_cred[_client]['api_secret']

        req_token=getkite(_client)  
        print('Req Token-> ' + req_token)
        # req_token = '8DoJtcPaDkOEj0bxCOm4KC7u4Y3QUd8H'
        url  = 'https://kite.trade/connect/login?v=3&api_key='+api_key 
        print ('url-',url)
        # pdb.set_trace()
        # telegram_bot_sendtext("Line 186")
        # pdb.set_trace()
        kite = KiteConnect(api_key=api_key)
        data = kite.generate_session(req_token, api_secret=api_secret)
        access_token=data["access_token"]
        # print(data['user_name'],'has successfully signed in.')
        print('Access_token->',access_token)
        auth_keys[_client] = access_token

        auth_keys['date'] = cur_date
        # telegram_bot_sendtext("Auth keys extracted!\n\nUser = \t\t" + _client   +  "\nAuth Key = \t" + auth_keys[_client] +  "\nDate = \t" + auth_keys['date'])

    return access_token

if __name__ == '__main__':
    try:
        print(gen_acc_token())
        
    except Exception as e:
        print('Happy Trading !')
        # print(my_api_key,acc_key)
        #telegram_bot_sendtext(f" Error in Token Generation - {str(e)}")