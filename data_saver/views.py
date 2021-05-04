from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def home(request):
    if request.method=='GET':
        print('home called')
        return render(request, 'index.html')
    elif request.method=='POST':
        print(request.POST)
        print(request)
    return redirect('home')



# working for opencv// needs ajax here
import numpy as np
import cv2 as cv


def open_cam(request):
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        normal = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Display the resulting frame
        cv.imshow('frame', normal)
        break
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cv.imshow('frame', normal)
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("saved_webcam.png", normal)
    cap.release()
    cv.destroyAllWindows()
    return HttpResponse('Hello there')