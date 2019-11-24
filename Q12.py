""" Q12 Trivia Automator:
    Working:
    - Duplicate mobile phone's app in your pc (Vysor, for example). Lag consideration is important here.
    - Screenshot the screen, and perform OCR on the questions and answers.
    - Try to find the most probable answer using Google.
"""


import pyscreenshot as ss
# from PIL import Image
import pytesseract  # OCR
# WebScraping
import requests
from bs4 import BeautifulSoup


while True:

    # Screenshots
    lines = int(input())  # number of lines in question (visualy recognized)

    # ###### small questions #########
    bottom = 605

    q = ss.grab(bbox=(35, bottom - 33*lines, 410, bottom))  # Question

    # Answers
    r1 = ss.grab(bbox=(65, 646, 395, 676))
    r2 = ss.grab(bbox=(65, 717, 395, 747))
    r3 = ss.grab(bbox=(65, 788, 395, 824))

    # ####### Big questions #########
    # bottom = 530
    #
    # q = ss.grab(bbox=(45, bottom - 45*lines, 415, bottom))  # Question
    # # Answers
    # r1 = ss.grab(bbox=(70, 574, 380, 610))
    # r2 = ss.grab(bbox=(70, 668, 380, 705))
    # r3 = ss.grab(bbox=(70, 764, 380, 800))

    # q.show()
    # r1.show()
    # r2.show()
    # r3.show()

    # OCR (Image to text)

    Q = pytesseract.image_to_string(q, lang='spa')
    R1 = pytesseract.image_to_string(r1, lang='spa')
    R2 = pytesseract.image_to_string(r2, lang='spa')
    R3 = pytesseract.image_to_string(r3, lang='spa')

    # print(pytesseract.image_to_string(q, lang='spa'))
    # print(pytesseract.image_to_string(r1, lang='spa'))
    # print(pytesseract.image_to_string(r2, lang='spa'))
    # print(pytesseract.image_to_string(r3, lang='spa'))

    # print(Q)
    # print(R1)
    # print(R2)
    # print(R3)
    # Text for Google. Each answer is looked up together with the question using Google's search options

    T1 = Q + ' ' + R1 + ' -"' + R2 + '" -"' + R3 + '"'
    T2 = Q + ' ' + R2 + ' -"' + R1 + '" -"' + R3 + '"'
    T3 = Q + ' ' + R3 + ' -"' + R1 + '" -"' + R2 + '"'

    # T1 = Q + ' ' + R1
    # T2 = Q + ' ' + R2
    # T3 = Q + ' ' + R3

    r = requests.get('http://www.google.es/search',
                     params={'q': T1}
                     )

    soup = BeautifulSoup(r.text, 'html5lib')

    N1 = soup.find('div', {'id': 'resultStats'}).text

    r = requests.get('http://www.google.es/search',
                     params={'q': T2}
                     )

    soup = BeautifulSoup(r.text, 'html5lib')

    N2 = soup.find('div', {'id': 'resultStats'}).text

    r = requests.get('http://www.google.es/search',
                     params={'q': T3}
                     )

    soup = BeautifulSoup(r.text, 'html5lib')

    N3 = soup.find('div', {'id': 'resultStats'}).text  # takes the number of results for each answer

    # # Reference values (only looking the question)

    # r = requests.get('http://www.google.es/search',
    #                  params={'q': R1}
    #                  )
    #
    # soup = BeautifulSoup(r.text, 'html5lib')
    #
    # P1 = soup.find('div', {'id': 'resultStats'}).text
    #
    # r = requests.get('http://www.google.es/search',
    #                  params={'q': R2}
    #                  )
    #
    # soup = BeautifulSoup(r.text, 'html5lib')
    #
    # P2 = soup.find('div', {'id': 'resultStats'}).text
    #
    # r = requests.get('http://www.google.es/search',
    #                  params={'q': R3}
    #                  )
    #
    # soup = BeautifulSoup(r.text, 'html5lib')
    #
    # P3 = soup.find('div', {'id': 'resultStats'}).text

    # N1 = float(N1[16:-11])
    # N2 = float(N2[16:-11])
    # N3 = float(N3[16:-11])

    # Finally you decide wich answer is the most probable one, and select it in the app
    print(R1 + ' ' + N1)
    print(R2 + ' ' + N2)
    print(R3 + ' ' + N3)

    # print(T1)
    # print(T2)
    # print(T3)
