# Contact sheet of rendered stills (no reference footage for the P clips).
# python hf/_chatly/sheet.py <assetDir> <tag> k1 k2 ...   (k = frame index at 24 fps)
import sys,os,cv2,numpy as np
d,tag=sys.argv[1],sys.argv[2];ks=[int(x) for x in sys.argv[3:]];os.makedirs(f'{d}/qa',exist_ok=True);tiles=[]
for k in ks:
    im=cv2.imread(f'{d}/tmp/frames/k{k:04d}.png',cv2.IMREAD_UNCHANGED)
    if im is None: continue
    if im.shape[2]==4:
        a=im[...,3:4]/255.;chk=np.indices(im.shape[:2]).sum(0)//24%2*40+90;im=(im[...,:3]*a+chk[...,None]*(1-a)).astype(np.uint8)
    im=cv2.resize(im,(720,540));cv2.putText(im,f'k{k} t={k/24:.2f}s',(10,30),0,.9,(0,0,255),2);tiles.append(im)
while len(tiles)%2: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+2]) for i in range(0,len(tiles),2)]
for i in range(0,len(rows),3): cv2.imwrite(f'{d}/qa/{tag}_{i//3:02d}.jpg',np.vstack(rows[i:i+3]),[cv2.IMWRITE_JPEG_QUALITY,85])
print('ok',len(tiles))
