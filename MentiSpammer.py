import requests as rq
import os
import threading
from urllib.request import Request, urlopen
import random
import json


print("""
\33[32m
         ,---.  .-. .-. _______ ,-.     .---. ,---.    .--.           
|\    /| | .-'  |  \| ||__   __||(|    ( .-._)| .-.\  / /\ \ |\    /| 
|(\  / | | `-.  |   | |  )| |   (_)   (_) \   | |-' )/ /__\ \|(\  / | 
(_)\/  | | .-'  | |\  | (_) |   | |   _  \ \  | |--' |  __  |(_)\/  | 
| \  / | |  `--.| | |)|   | |   | |  ( `-'  ) | |    | |  |)|| \  / | 
| |\/| | /( __.'/(  (_)   `-'   `-'   `----'  /(     |_|  (_)| |\/| | 
'-'  '-'(__)   (__)                        (__)            '-'  '-'       

---------------------------------------------------------------------

\33[37m
""")




MentID = input("\033[0mEnter MentiID:\n> ")
Threads = int(input("Threads:\n> "))
POST_HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

POST_DATA = {
    "question_type": "wordcloud"
}
ThreadCount = int(0)


def MENTI_IDENTIFIER():
    try:
        IDENTI_REQ = rq.post("https://www.menti.com/core/identifiers", headers=POST_HEADER)
    except:
         return print(f"\033[31m[ERROR] An unknown error occured on request identifiers!\33[37m")

    IDENTI_RES = json.loads(IDENTI_REQ.text)
    IDENTI = IDENTI_RES["identifier"]
    return IDENTI



def MENTI_INFO(menti_ID: str):
    # Fetch Info from Menti
    INFO_Request = rq.get(f"https://www.menti.com/core/vote-keys/{menti_ID}/series", headers=POST_HEADER)

    # Error Handeling
    if INFO_Request.status_code != 200:
        return 0


    # Return on Success
    Response = json.loads(INFO_Request.text)
    return Response["pace"]["active"] 



def POST_WORD(post_word: list, identifier: str, public_key: str):    
    # Empty Check -> Possible Broken Wordlist API
    if post_word == "":
        print("\033[31m[ERROR] Empty Wordlist!\33[37m")
        return
    

    # Post New Word to Menti
    POST_HEADER["x-identifier"] = identifier
    POST_DATA["vote"] = post_word
    try:
        post_word_request = rq.post(f"https://www.menti.com/core/votes/{public_key}", headers=POST_HEADER, data=POST_DATA)
    except:
        return print(f"\033[31m[ERROR] An unknown error occured on posting word: {post_word}\33[37m")
    



    # Error Handeling + Console Output
    if post_word_request.status_code == 200:
        print(f"\033[92m[INFO] Posted word: {post_word}       ({threading.current_thread().name})\33[37m")
    else :
        print(f"\033[31m[ERROR] An error occured on posting word: {post_word_request.status_code}\33[37m")


def MENTISPAMMER(word_list: list, public_key: str):
    # Spammer Class -> Spam Until Hard Close

    print(f"\033[93m[INFO] {threading.current_thread().name} started!\33[37m")


    # Endless Loop until Kill
    while 1:
        for word in word_list:
            identifier = MENTI_IDENTIFIER()
            POST_WORD(random.choice(word_list), identifier, public_key)


def main():

    # Get Random Word List
    wordlist = rq.get("https://random-word-api.herokuapp.com/word?number=50000").json()
    print(f"\n\033[95m[INFO] Prepared Wordlist ({len(wordlist)} words)\33[37m")

   
    # Get Menti Public Key
    public_key = MENTI_INFO(MentID)
    if public_key == 0:
        print(f"\033[31m[ERROR] There was an error on requesting informations from Menti!\n\n\033[1mCheck if the Menti-ID is valid!\33[37m")
        quit()


    # Start Threads + Spammer
    for _ in range(Threads):
        thread = threading.Thread(target=MENTISPAMMER,args=(wordlist, public_key))
        thread.start()
        
if __name__=='__main__':
    main()
