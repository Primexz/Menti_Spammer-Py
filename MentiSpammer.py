import requests as rq
import os
import threading
from urllib.request import Request, urlopen
import random
import json

MentID = input("Enter MentiID:\n> ")
Threads = int(input("Threads:\n> "))
POST_HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " 
    + "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
POST_DATA = {
    "question_type": "wordcloud"
}
MENTI_IDENTIFIERS = "https://www.menti.com/core/identifiers"
IDENTIFIERS = []
ThreadCount = int(0)


def MENTI_IDENTIFIER():
    identifier_request = rq.post(MENTI_IDENTIFIERS, headers=POST_HEADER)

    identifier_response = json.loads(identifier_request.text)
    identifier = identifier_response["identifier"]
    IDENTIFIERS.append(identifier)
    return identifier



def MENTI_INFO(menti_ID: str):
    # Fetch Info from Menti
    series_URL = f"https://www.menti.com/core/vote-keys/{menti_ID}/series"
    series_request = rq.get(series_URL, headers=POST_HEADER)
    
    series_response = json.loads(series_request.text)
    return series_response


def POST_WORD(word_list: list, identifier: str, public_key: str):    
    # Empty Check -> Possible Broken Wordlist API
    if word_list == "":
        print("Oops, the fetched Wordlist is empty?")
        return
    
    # Post New Word to Menti
    POST_HEADER["x-identifier"] = identifier
    vote_str = " ".join([word.replace(" ","_") for word in word_list])
    POST_DATA["vote"] = vote_str
    post_word_URL = f"https://www.menti.com/core/votes/{public_key}"
    post_word_request = rq.post(post_word_URL, headers=POST_HEADER, data=POST_DATA)
    print("[INFO] Posted word: {}       ({})".format(vote_str, threading.current_thread().name))
    



def MENTISPAMMER(word_list: list, public_key: str):
    # Spammer Class -> Spam Until Hard Close

    print("[INFO] {} started!".format(threading.current_thread().name))

    while 1:
        for word in word_list:
            identifier = MENTI_IDENTIFIER()
            POST_WORD(word, identifier, public_key)



def main():

    # Get Random Word List + Shuffle + Cut Array to 1000 Words
    url="https://svnweb.freebsd.org/csrg/share/dict/words?revision=61569&view=co"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    wordlist = web_byte.decode('utf-8')
    wordlist = wordlist.split("\n")
    random.shuffle(wordlist)
    print("[INFO] Prepared Wordlist ({} words)".format(len(wordlist)))


    # Get Menti Public Key
    public_key = MENTI_INFO(MentID)["pace"]["active"] 

    print("[INFO] Starting Threads..")
    # Start Threads + Spammer
    for _ in range(Threads):
        thread = threading.Thread(target=MENTISPAMMER,args=(wordlist, public_key))
        thread.start()
        
if __name__=='__main__':
    main()
