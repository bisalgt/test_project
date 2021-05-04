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
    print(request.GET["value"], '---------------')
    request.session["checker"] = request.GET["value"]
    if request.session["checker"] ==  'start':
        print("session running")

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # print("Inside while")
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print(ret)
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        normal = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Display the resulting frame
        cv.imshow('frame', normal)

        # check request session values
        if request.session["checker"] ==  'save':
            print("image saved")
            cv.imwrite("saved_cam.png", normal)
        cv.waitKey(10)
        if request.session["checker"] ==  'stop':
            print("session stopped")
            break
    cap.release()
    cv.destroyAllWindows()
    return HttpResponse('Hello there')

def click_done(request):
    cv.destroyAllWindows()
    return HttpResponse("Destroyed all windows")