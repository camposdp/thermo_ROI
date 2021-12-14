import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import keyboard
from os import walk
import re


def normalize(M):
    max = np.amax(M)
    min = np.amin(M)
    M_norm = (M-min)/(max - min)
    return M_norm

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping, roi
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)       
           
def getROI(path,pre):     
    
 

    global cropping, refPoint, oriImage, x_start, y_start, x_end, y_end, roi
    
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    x_1, y_1, x_1, y_1 = 0, 0, 0, 0
    

    df = pd.read_csv(path,sep=',',decimal=".")
    
    ########## Código ##########
    
    #Convert the dataframe to array
    arr = df.to_numpy()
    
    #Normalize the array
    arr_norm = normalize(arr)
    img = arr_norm
    scale_percent = 300 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    
    #Muda a escala da imagem
    imgrsz = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    
    #Chama função de cropp para a ação do clique do mouse
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    
    
    
    #Mostra imagem
    colormap = plt.get_cmap('inferno')
    heatmap = (colormap(imgrsz) * 2**16).astype(np.uint16)[:,:,:3]
    image = cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR)
    oriImage = image.copy()
    
    
    
    #Laço do crop (Aperte Q para sair)
    while True:
    
        i = image.copy()
        if not cropping:
    
            cv2.imshow("image", image)
            #cv2.imshow('heatmap', heatmap)
           
           
        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv2.imshow("image", i)
           
        if keyboard.is_pressed("d"):
            print("Perna Direita")
            lado = 'd'
            break
    
        if keyboard.is_pressed("e"):
            print("Perna Esquerda")
            lado = 'e'
            break        
        
 
        cv2.waitKey(1)  
       
           


   #Fecha todas as imagens
    cv2.destroyAllWindows()
    cv2.waitKey(1)  
    
    #converte o retângulo para escala original    
    x_1 = int(x_start *100 / scale_percent)
    x_2 = int(x_end *100 / scale_percent)
    y_1 = int(y_start *100 / scale_percent)
    y_2 = int(y_end *100 / scale_percent)
    refPoint = [(x_1, y_1), (x_2, y_2)]
    
    dx=abs(x_2-x_1)
    dy=abs(y_2-y_1)
    
    #inicial/final baseado no menor valor
    #evita problemas se o quadrado começa da direita para a esquerda
    xi = min(x_1,x_2)
    xf = max(x_1,x_2)
    yi = min(y_1,y_2)
    yf = max(y_1,y_2)
    
    if dy>dx:
        print('Em pé')
        #Segmenta a imagem
        #Separa em porções 15/70/15
        pos = 'E'
    
        #distal
        roi_d = arr[yi:round(yi+dy*0.15), xi:xf]
        
        #medial
        roi_m = arr[round(yi+dy*0.15):round(yi+dy*0.85), xi:xf]
        
        #proximal
        roi_p = arr[round(yi+dy*0.85):yf, xi:xf]   
        
        dataformat = '.csv'
    
        np.savetxt(pre+pos+'_'+'d'+lado+dataformat, roi_d, delimiter=",")
        np.savetxt(pre+pos+'_'+'m'+lado+dataformat, roi_m, delimiter=",")
        np.savetxt(pre+pos+'_'+'p'+lado+dataformat, roi_p, delimiter=",")
        print('Salvo!')    
    
        
    
        
    if dx>dy:
        print('Deitado')
        pos = 'D'
        #Segmenta a imagem
        #Separa em porções 15/70/15
    
        #distal
        roi_d = arr[yi:yf, xi:round(xi+dx*0.15)]
        
        #medial
        roi_m = arr[yi:yf, round(xi+dx*0.15):round(xi+dx*0.85)]
        
        #proximal
        roi_p = arr[yi:yf,round(xi+dx*0.85):xf] 
        
    
        
    
        dataformat = '.csv'
    
        np.savetxt(pre+pos+'_'+'d'+lado+dataformat, roi_d, delimiter=",")
        np.savetxt(pre+pos+'_'+'m'+lado+dataformat, roi_m, delimiter=",")
        np.savetxt(pre+pos+'_'+'p'+lado+dataformat, roi_p, delimiter=",")
        print('Salvo!')
        


    
    
    

    
    
def readFolders(mypath):
    
    
    
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    print("Onde começar? \n\n")
    for (i, item) in enumerate(dirnames, start=1):
        print(i, item)
    start=int(input("\n \n Digite o número da pasta...\n Pasta = "))
        
    length = len(dirnames)
    for i in range(start-1,length):
        g = []
        for (dirpath2, dirnames2, filenames2) in walk(mypath+"\\"+dirnames[i]):
            g.extend(filenames2)
            break
        length2 = len(dirnames2)
        
        for j in range(length2):
      
            h = []
            for (dirpath3, dirnames3, filenames3) in walk(mypath+"\\"+dirnames[i]+"\\"+dirnames2[j]):
                h.extend(filenames)
                break
            
            n=j+1
            txt = dirnames[i]
            
            age=re.findall(r'\d+',txt)
            sxStr=dirnames[i].find("Feminino")
            if sxStr<0:
                sx = "M"
            else:
                sx = "F"
                
            print(dirnames2[j])
            pre = str(n).zfill(2)+"_"+txt[0]+sx+age[0]   
            lst=[i for i in filenames3 if i.endswith('.csv')]
            fullpath = mypath+"\\"+dirnames[i]+"\\"+dirnames2[j]
            dataformat = '.csv'
            file1 = fullpath + "\\" + lst[2]
            file2 = fullpath + "\\" + lst[3]
            
            print("Selecione a perna direita")
            getROI(file1,pre)
            print("Selecione a perna esquerda")
            getROI(file1,pre)            
            print("Selecione a perna direita")
            getROI(file2,pre)
            print("Selecione a perna esquerda")
            getROI(file2,pre)
            x = input("Continuar (Enter) / Sair (q)...\n")
            if x == 'q':
                break
         
            