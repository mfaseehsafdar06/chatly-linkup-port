# Detect photo windows / grey slots in the cutouts (normalised to each cutout's alpha-trimmed bbox).
# Re-run whenever assets/cut changes:  python detect.py  -> detect.json
import cv2,numpy as np,json
C='../../assets/cut/'
def trimbox(im):
    if im.shape[2]==3: return 0,0,im.shape[1],im.shape[0]
    ys,xs=np.where(im[...,3]>128); return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def grey(name):
    im=cv2.imread(C+name+'.png',cv2.IMREAD_UNCHANGED); x0,y0,x1,y1=trimbox(im); im=im[y0:y1,x0:x1]
    rgb=im[...,:3].astype(int); mn=rgb.min(2); mx=rgb.max(2)
    m=((mx-mn)<14)&(mn>150)&(mx<245)
    if im.shape[2]==4: m&=im[...,3]>200
    m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_OPEN,np.ones((7,7),np.uint8))
    n,l,s,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(s[1:,4]); x,y,w,h=s[k,:4]
    H,W=im.shape[:2]; return [round(x/W,4),round(y/H,4),round((x+w)/W,4),round((y+h)/H,4)]
def red(name):
    im=cv2.imread(C+name+'.png',cv2.IMREAD_UNCHANGED); x0,y0,x1,y1=trimbox(im); im=im[y0:y1,x0:x1]
    hsv=cv2.cvtColor(im[...,:3],cv2.COLOR_BGR2HSV); m=(((hsv[...,0]<10)|(hsv[...,0]>170))&(hsv[...,1]>120)&(hsv[...,2]>90)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8)); n,l,s,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(s[1:,4]); x,y,w,h=s[k,:4]
    H,W=im.shape[:2]; return [round(x/W,4),round(y/H,4),round((x+w)/W,4),round((y+h)/H,4)]
out={'GPT-03_00':grey('GPT-03_00'),'GPT-03_00_red':red('GPT-03_00')}
for i in range(5): out[f'GPT-08_0{i}']=grey(f'GPT-08_0{i}')
json.dump(out,open('detect.json','w'),indent=1); print(out)
