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
    global folder_name
    i = 0
    print(request.session.items(), 'inside home first ')
    if request.method=='GET':
        if request.session.keys() is not None:
            print("Session is not none so deleting the old session")
            keys = dict(request.session.items()).keys()
            for key in keys:
                del request.session[key]
        print('home called')
        return render(request, 'index.html')
    elif request.method=='POST':
        folder_name = folder_name
        images = request.session.get('images')
        files = request.FILES.getlist("fileholder")
        fs = FileSystemStorage()
        # createFolder(f'data/{name}')
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, folder_name)
        for file in files:
            fs.save(file.name, file)
        
    print(request.session.items(), '00000000000000000000000000   after submitting')
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
folder_name = ''
def open_cam(request):
    global i
    global folder_name
    print(request.GET["value"], '---------------')
    request.session["checker"] = request.GET["value"]
    if request.session["checker"] ==  'start':
        print("session running")
        name = request.GET["name"]
        folder_name = f'data/{name}'
        createFolder(folder_name)
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
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
            name_to_save = f'image_{i}'
            request.session[name_to_save] = i
            print('print the request the session', request.session.items())
            image_name = f"{folder_name}/changed_img_{i}.png"
            cv.imwrite(image_name, np.array(normal.tolist()))
            i += 1
            print("image saved")
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