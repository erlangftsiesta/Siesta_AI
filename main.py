import speech_recognition as sVoice
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pywhatkit as kit
import openai
import os
import webbrowser
from gtts import gTTS

# Setup kunci API OpenAI
openai.api_key = "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"

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setup koneksi dengan Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='af69d612b4b147e4aae30af4fcb6f0b9',
                                               client_secret='b36f44c719a54a13876dcaef58f626d2',
                                               redirect_uri='https://github.com/erlangftsiesta',
                                               scope='user-library-read user-read-playback-state user-modify-playback-state'))

def play_spotify_track(track_name):
    results = sp.search(q=track_name, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Memutar lagu: {results['tracks']['items'][0]['name']}")
    else:
        print("Lagu tidak ditemukan.")

def speech_to_text():
    recognizer = sVoice.Recognizer()
    microphone = sVoice.Microphone()

    with microphone as source:
        print('Mendengarkan...')
        audio = recognizer.listen(source, phrase_time_limit=7)
        try:
            print('Memproses...')
            teks = recognizer.recognize_google(audio, language='id-ID')
            print('Anda mengatakan:', teks)
            return teks
        except sVoice.UnknownValueError:
            print("Maaf, tidak dapat mengerti suara.")
            return None
        except sVoice.RequestError:
            print("Tidak dapat meminta hasil. Periksa koneksi jaringan Anda.")
            return None

def text_to_speech(teks):
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
         if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(teks)
    engine.runAndWait()

def chat_dengan_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

def start_conversation():
    print("Berbincang dengan AI...")
    searching_mode = True  # Tandai bahwa awalnya sedang dalam mode pencarian
    while True:
        input_pengguna = speech_to_text()

        if input_pengguna:
            if "hentikan system" in input_pengguna.lower():
                print("Mengakhiri percakapan dengan AI.")
                text_to_speech("Percakapan dengan AI dihentikan.")
                break
            elif "matikan Sistem" in input_pengguna.lower():
                print("System akan dimatikan")
                text_to_speech("System will be Shutdown!, have a nice day!")
                os._exit(0)
            elif "keluar dari mode pencarian" in input_pengguna.lower():
                text_to_speech("Out of Searching mode. Now in Standby Mode")
                searching_mode = False  # Keluar dari mode pencarian
            
            else:
                if searching_mode:
                    # Lakukan tindakan saat berada dalam mode pencarian
                    respons_gpt = chat_dengan_gpt(input_pengguna)
                    print("Respons AI:", respons_gpt)
                    text_to_speech(respons_gpt)

def wait_for_trigger(trigger_phrase):
    recognizer = sVoice.Recognizer()
    microphone = sVoice.Microphone()

    while True:
        print("Menunggu perintah...")
        trigger_input = speech_to_text()

        if trigger_input and trigger_phrase.lower() in trigger_input.lower():
            print("Perintah terdeteksi:", trigger_phrase)
            break

if __name__ == "__main__":
    while True:
        print("Menunggu trigger")
        wait_for_trigger("Hello Jarvis") #KALO UDAH KETEMU MODUL SUARA CWEKNYA, UBAH LAGI KE SIESTA Y!
        print("Bot Diaktifkan...")
        text_to_speech("Halo!, How was ur Day? I'm Your Assistent ready to Help, Erlang")

        while True:
            print("Silakan berkata sesuatu...")
            input_pengguna = speech_to_text()

            if input_pengguna:
                if "hentikan system" in input_pengguna.lower():
                    print("Menghentikan sistem.")
                    text_to_speech("Selamat tinggal!")
                    wait_for_trigger("Halo Siesta")
                elif "mode terjaga" in input_pengguna.lower():
                    print("Memasuki Mode Stand By.")
                    text_to_speech("Stand By mode has been Activated!")
                    wait_for_trigger("Hello Jarvis")
                elif "buka youtube" in input_pengguna.lower():
                    search_query = input_pengguna.replace("cari di youtube", "")
                    print("Mencari di YouTube:", search_query)
                    text_to_speech(f"Mencari di YouTube: {search_query}")
                    kit.playonyt(search_query)
                elif "cari data" in input_pengguna.lower():
                    search_query = input_pengguna.replace("cari di internet", "")
                    print("Mencari Data di Internet:", search_query)
                    text_to_speech(f"Perintah disimpan, mencari data: {search_query}")
                    kit.search(search_query)
                elif "setel lagu" in input_pengguna.lower():
                    search_query = input_pengguna.replace("").strip()
                    print("Mencari lagu di Spotify:", search_query)
                    webbrowser.open(f"https://open.spotify.com/search/{search_query}")
                    text_to_speech(f"Membuka lagu {search_query} di Spotify.")
                elif "matikan System" in input_pengguna.lower():
                    print("System akan dimatikan")
                    text_to_speech("System will be Shutdown!, have a nice day!")
                    os._exit(0)
                elif "aktifkan mode pencarian" in input_pengguna.lower():
                    print("Memasuki Mode Searching")
                    text_to_speech("U want me to Search info like what?")
                    start_conversation()
            else:
                print("Pengguna belum memberikan input")

























# def speech_to_text():
#     recognizer = sVoice.Recognizer()
#     microphone = sVoice.Microphone()

#     with microphone as source:
#         print('Mendengarkan...')
#         audio = recognizer.listen(source, phrase_time_limit=5)
#         try:
#             print('Memproses...')
#             text = recognizer.recognize_google(audio, language='id-ID')
#             print('Anda mengatakan:', text)
#             return text
#         except sVoice.UnknownValueError:
#             print("Maaf, tidak dapat mengerti suara.")
#             return None
#         except sVoice.RequestError:
#             print("Tidak dapat meminta hasil. Periksa koneksi jaringan Anda.")
#             return None

# def text_to_speech(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# def search_wikipedia(query):
#     try:
#         summary = wikipedia.summary(query, sentences=2)
#         return summary
#     except wikipedia.exceptions.PageError:
#         return "Maaf, saya tidak dapat menemukan informasi tentang itu."
#     except wikipedia.exceptions.DisambiguationError:
#         return "Terdapat beberapa kemungkinan hasil. Mohon berikan informasi yang lebih spesifik."
#     except wikipedia.exceptions.HTTPTimeoutError:
#         return "Waktu pencarian di Wikipedia habis. Mohon coba lagi nanti."

# if __name__ == "__main__":
#     while True:
#         print("Silakan berkata sesuatu...")
#         user_input = speech_to_text()

#         if user_input:
#             if "berhenti" in user_input.lower():
#                 print("Menghentikan sistem.")
#                 text_to_speech("Sampai jumpa, Erlang!")
#                 break
            
#             print("Mencari di Wikipedia untuk:", user_input)
#             wiki_result = search_wikipedia(user_input)
#             print("Ringkasan Wikipedia:", wiki_result)
#             text_to_speech(wiki_result)























# def perintah():
#     dengar = sVoice.Recognizer() #Mengambil atribut Objek sVoice
#     with sVoice.Microphone() as src: #Membuat sebuah Perintah
#         print('Listening . . .')
#         suara = dengar.listen(src, phrase_time_limit=5)
#         try:
#             print('Processing. . .')
#             Service = dengar.recognize_google(suara, language='id-ID')
#             print(Service)
#         except:
#             pass
#         return Service

# def knowledge():
#     In = 
#     voice = pyt.init()
#     result = wikipedia.summary

# def bicara(self):
#     teks = (self) 
#     bahasa = 'id'
#     namaFile = 'bicara.mp3'
#     def read():
#         suara = gTTS(text=teks, lang=bahasa, slow=False)
#         suara.save(namaFile)
#         os.system(f'start {namaFile}')
#     read( )

# def startSiesta():
#     Service = perintah()
#     bicara(Service)

# startSiesta()