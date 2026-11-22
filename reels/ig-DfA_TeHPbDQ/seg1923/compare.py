# python compare.py <framesdir> <tag> k1 k2 ...   -> qa/<tag>_pairs_XX.jpg (ref left | mine right)
import sys,cv2,numpy as np,os
fd,tag=sys.argv[1],sys.argv[2];ks=[int(x) for x in sys.argv[3:]]
os.makedirs('qa',exist_ok=True)
rows=[]
for k in ks:
    r=cv2.resize(cv2.imread(f'ref24/r{k+4:03d}.png'),(720,540),interpolation=cv2.INTER_AREA)
    m=cv2.resize(cv2.imread(f'{fd}/k{k:03d}.png'),(720,540),interpolation=cv2.INTER_AREA)
    row=np.hstack([r,np.full((540,8,3),255,np.uint8),m])
    cv2.putText(row,f'k{k} n{k+4} t={19+(k+4)/24:.3f}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,.9,(0,255,255),2)
    rows.append(row)
for i in range(0,len(rows),3):
    sheet=np.vstack([np.vstack([x,np.full((8,x.shape[1],3),255,np.uint8)]) for x in rows[i:i+3]])
    cv2.imwrite(f'qa/{tag}_{i//3:02d}.jpg',sheet,[cv2.IMWRITE_JPEG_QUALITY,85])
print('ok')
