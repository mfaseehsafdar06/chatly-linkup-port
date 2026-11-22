# QA video for alpha assets: post frames composited over the matching reference frames (QA ONLY — contains ref pixels).
# python qa_video.py <assetDir> <refStartFrame>   -> <asset>/qa/<name>-QA-over-ref.mp4 (left: ref, right: ours over ref)
import sys,os,glob,subprocess,cv2,numpy as np
d,K0=os.path.abspath(sys.argv[1]),int(sys.argv[2]); name=os.path.basename(d)
REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','refs','ref.mp4')
fs=sorted(glob.glob(f'{d}/tmp/post/k*.png')) or sorted(glob.glob(f'{d}/tmp/frames/k*.png')); n=len(fs)
T=f'{d}/tmp/_qa'; os.makedirs(T,exist_ok=True); [os.remove(x) for x in glob.glob(T+'/*')]
subprocess.run(['ffmpeg','-v','error','-i',REF,'-vf',f'select=between(n\\,{K0}\\,{K0+n-1}),scale=1440:1080','-fps_mode','passthrough',f'{T}/r%04d.png'],check=True)
rs=sorted(glob.glob(T+'/r*.png'))
for i,p in enumerate(fs):
    m=cv2.imread(p,cv2.IMREAD_UNCHANGED); r=cv2.imread(rs[min(i,len(rs)-1)]).astype(np.float32)
    c=m[...,:3]*(m[...,3:4]/255.)+r*(1-m[...,3:4]/255.) if m.shape[2]==4 else m
    cv2.imwrite(f'{T}/q{i:04d}.png',np.hstack([cv2.resize(r,(720,540)),cv2.resize(c.astype(np.float32),(720,540))]).astype(np.uint8))
os.makedirs(f'{d}/qa',exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',f'{T}/q%04d.png','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',f'{d}/qa/{name}-QA-over-ref.mp4'],check=True)
subprocess.run(['rm','-rf',T]); print('qa video',n)
