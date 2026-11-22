import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
SH=[(22,'1','Crayon globe','"all over the world" pops in word by word',0,26),
    (40,'2','Singapore','Marker circles Singapore',27,44),
    (56,'3','Australia','Circle drawn counter-clockwise',45,58),
    (68,'4','Canada','Marker enters from the left',59,69),
    (80,'5','New York','"NY!" written, circle, dot',70,83),
    (92,'6','UK','Circle around the UK',84,94),
    (96,'7','Whip-zoom','Fast zoom out with motion blur',95,97),
    (101,'8','Full map','Every mark visible',98,101)]
f=lambda s,b=False:ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',s,index=1 if b else 0)
TW,TH=640,480;RW,RH=200,150;PAD=36;CW=TW;CH=TH+RH+110
cols=4;W=PAD+cols*(CW+PAD);H=150+2*(CH+PAD)
sb=Image.new('RGB',(W,H),(246,245,241));d=ImageDraw.Draw(sb)
d.text((PAD,40),'Storyboard: 19.2–23.4 s (globe + map)',font=f(46,True),fill=(20,20,24))
d.text((PAD,98),'8 shots · 4.25 s · 4:3 · 24 fps   |   large = ours, small = reference at the same frame',font=f(24),fill=(90,90,96))
for i,(k,n,t,desc,k0,k1) in enumerate(SH):
    x=PAD+(i%cols)*(CW+PAD);y=150+(i//cols)*(CH+PAD)
    m=Image.open(f'frames_v9g/k{k:03d}.png').convert('RGB').resize((TW,TH),Image.LANCZOS)
    r=Image.open(f'ref24/r{k+4:03d}.png').convert('RGB').resize((RW,RH),Image.LANCZOS)
    sb.paste(m,(x,y));d.rectangle([x,y,x+TW-1,y+TH-1],outline=(200,200,200))
    d.rounded_rectangle([x+12,y+12,x+62,y+62],10,fill=(20,20,24));d.text((x+37,y+37),n,font=f(30,True),fill='white',anchor='mm')
    sb.paste(r,(x+TW-RW,y+TH+14));d.text((x+TW-RW,y+TH+14+RH+6),'reference',font=f(18),fill=(120,120,126))
    t0=19+(k0+4)/24;t1=19+(k1+5)/24
    d.text((x,y+TH+14),t,font=f(32,True),fill=(20,20,24))
    d.text((x,y+TH+58),f'{t0:.2f}–{t1:.2f} s  ({k1-k0+1} fr)',font=f(22),fill=(110,110,116))
    yy=y+TH+92
    words=desc.split();line=''
    for w_ in words:
        if d.textlength(line+' '+w_,font=f(22))>TW-RW-24: d.text((x,yy),line.strip(),font=f(22),fill=(50,50,56));yy+=30;line=''
        line+=' '+w_
    d.text((x,yy),line.strip(),font=f(22),fill=(50,50,56))
sb.save('out/seg1923-storyboard.png');print(sb.size)
