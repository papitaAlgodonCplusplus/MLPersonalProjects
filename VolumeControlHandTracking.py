import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import mediapipe as mp

cap = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
sessions = AudioUtilities.GetAllSessions()

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
     dibujar = False
     success, img = cap.read()
     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     results = hands.process(imgRGB)

     if results.multi_hand_landmarks:
          for handLms in results.multi_hand_landmarks:
               for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                         dibujar = True
                         if cy > 470:
                          dibujar = False
                          cy = 500
                         if cy < 0:
                          dibujar = False
                          cy = 0
                         print(cy/500)
                         if dibujar == True:
                          cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                          mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                         for session in sessions:
                             volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                             if session.Process and session.Process.name() == "chrome.exe":
                                 volume.SetMasterVolume(1-(cy/500), None)
                         # -28.0 db to 0.0 db
     cv2.imshow("Image", img)
     cv2.waitKey(1)