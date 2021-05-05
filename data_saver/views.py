from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect

import os
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. '+ directory)
i = 0
@csrf_protect
def home(request):
    global i
    i = 0
    if request.method=='GET':
        request.session["images"] = []
        print('home called')
        return render(request, 'index.html')
    elif request.method=='POST':
        name = request.POST.get('name')
        images = request.session.get('images')
        files = request.FILES.getlist("fileholder")
        fs = FileSystemStorage()
        createFolder(f'data/{name}')
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, f'data/{name}')
        for file in files:
            fs.save(file.name, file)
        # print(len(images))
        # for index, image in enumerate(images):
        #     naming = f"data/{name}/from_webcam_{index}.png"
        #     cv.imwrite(naming, np.array(image, dtype='uint8'))
    return redirect('home')



# working for opencv// needs ajax here
import numpy as np
import cv2 as cv
import base64
import io
import matplotlib.pyplot as plt

def open_cam(request):
    global i
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
        cv.waitKey(10) #this give chance to run imshow so image can be seen on window
        # check request session values
        
        if request.session["checker"] ==  'save':
            print(i, ret, type(request.session["images"]))
            request.session["images"].append(i)
            cv.imwrite(f"data/changed_img_{i}.png", np.array(normal.tolist()))
            i += 1
            print("image saved")
            print(len(request.session["images"]), request.session["images"])
            request.session["checker"] = 'start'
        if request.session["checker"] ==  'stop':
            print("session stopped")
            break
    cap.release()
    cv.destroyAllWindows()
    return HttpResponse('hey there')

def click_done(request):
    print(request.session.items())
    return HttpResponse("Destroyed all windows")