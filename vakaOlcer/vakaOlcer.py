from bs4 import BeautifulSoup
import requests
import time
import RPi.GPIO as GPIO

key = "World"
worldmetersLink = "https://www.worldometers.info/coronavirus/"
data_check = []
toplam_vaka = []
toplam_vefat = []
toplam_taburcu = []

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    return

def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("+", "")
        i = i.replace("-", "")
        i = i.replace(",", "")
        i = i.replace(".", "")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L

counter = 0
while counter < 100:
    counter += 1
    html_page = requests.get(worldmetersLink)
    bs = BeautifulSoup(html_page.content, 'html.parser')
    search = bs.select("div tbody tr td")
    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(key) != -1:
            start = i
            break

    data = []
    for i in range(1, 6):
        data = data + [search[start + i].get_text()]
    data = data_cleanup(data)

    if data_check != data:
        data_check = data

        tvaka = int(data_check[0])
        tvefat = int(data_check[2])
        ttaburcu = int(data_check[4])

        toplam_vaka.append(tvaka)
        toplam_vefat.append(tvefat)
        toplam_taburcu.append(ttaburcu)
        
        if counter == 1:
            print("*********")
            print("Toplam Vaka Sayısı:", toplam_vaka[0], "Kişi")
            print("Toplam Vefat Sayısı:", toplam_vefat[0], "Kişi")
            print("Toplam İyilşen Sayısı:", toplam_taburcu[0], "Kişi")
            print("*********")

        elif counter > 1:
            toplam_vaka.reverse()
            toplam_vefat.reverse()
            toplam_taburcu.reverse()
            
            son_veri_vaka = int(toplam_vaka[0])
            son_veri_vefat = int(toplam_vefat[0])
            son_veri_taburcu = int(toplam_taburcu[0])
            
            onceki_veri_vaka = int(toplam_vaka[1])
            onceki_veri_vefat = int(toplam_vefat[1])
            onceki_veri_taburcu = int(toplam_taburcu[1])
            
            processResult_vaka = int(son_veri_vaka - onceki_veri_vaka)
            processResult_vefat = int(son_veri_vefat - onceki_veri_vefat)
            processResult_taburcu = int(son_veri_taburcu - onceki_veri_taburcu)
            
            print("Toplam Vaka'nın Veri Değişimi:", processResult_vaka, "Kişi")
            print("Toplam Vefat'ın Veri Değişimi:", processResult_vefat, "Kişi")
            print("Toplam Taburcu'nun Veri Değişimi:", processResult_taburcu, "Kişi")
            print("********************")
            
            toplam_vaka.reverse()
            toplam_vefat.reverse()
            toplam_taburcu.reverse()
            
            if processResult_vaka > (processResult_vefat and processResult_taburcu):
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(11, GPIO.OUT)  # kırmızıLed = Vaka
                for i in range(0, 10):
                    blink(11)
            elif processResult_vefat > (processResult_taburcu and processResult_vaka):
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(15, GPIO.OUT)  # sarıLed = Ölüm
                for i in range(0, 10):
                    blink(15)
            elif processResult_taburcu > (processResult_vaka and processResult_vefat):
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(18, GPIO.OUT)  # yesilLed = Taburcu
                for i in range(0, 10):
                    blink(18)
            else:
                print("Hata")
            GPIO.cleanup()
        else:
            print("Hata")
    else:
        time.sleep(60)
    time.sleep(60)
