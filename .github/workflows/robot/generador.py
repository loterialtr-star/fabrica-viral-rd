import os, feedparser, asyncio, edge_tts
from PIL import Image, ImageDraw, ImageFont
import textwrap

def buscar_noticia():
    feeds = ["https://www.listindiario.com/rss/portada","https://www.diariolibre.com/rss/portada","https://hoy.com.do/feed/"]
    for url in feeds:
        try:
            f = feedparser.parse(url)
            if f.entries:
                return f.entries[0].title, getattr(f.entries[0],'summary',f.entries[0].title)[:250]
        except: pass
    return "Ultima hora RD","Atencion, esto acaba de pasar en RD."

async def crear_voz(t):
    os.makedirs("output",exist_ok=True)
    comm = edge_tts.Communicate(t,"es-DO-JoseManuelNeural",rate="-10%",pitch="-20Hz")
    await comm.save("output/voz.mp3")

def crear_video(t):
    img=Image.new('RGB',(1080,1920),(5,5,5))
    d=ImageDraw.Draw(img)
    try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",65)
    except: f=ImageFont.load_default()
    y=550
    for lin in textwrap.wrap(t.upper(),22):
        d.text((80,y),lin,font=f,fill=(255,255,255))
        y+=90
    img.save("output/fondo.jpg")
    os.system('ffmpeg -y -loop 1 -i output/fondo.jpg -i output/voz.mp3 -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest -vf "scale=1080:1920,format=yuv420p" output/video_final.mp4')

if __name__=="__main__":
    titulo,res=buscar_noticia()
    asyncio.run(crear_voz(f"{titulo}. {res}. Sigueme para mas noticias RD."))
    crear_video(titulo)
