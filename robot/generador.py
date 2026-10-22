import os, feedparser, asyncio, edge_tts
from PIL import Image, ImageDraw, ImageFont
import textwrap

def buscar():
    try:
        f = feedparser.parse("https://www.listindiario.com/rss/portada")
        if f.entries and len(f.entries)>0:
            return f.entries[0].title
    except: pass
    return "Mensaje de la estrella del tarot para hoy"

async def voz(t):
    os.makedirs("output", exist_ok=True)
    # VOZ 100% SEGURA
    c = edge_tts.Communicate(t, "es-ES-AlvaroNeural")
    await c.save("output/voz.mp3")

def video(t):
    img = Image.new('RGB', (1080,1920), (15,15,40))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    y=650
    for lin in textwrap.wrap(t, 25):
        d.text((50,y), lin.upper(), font=font, fill=(255,215,0))
        y+=80
    img.save("output/fondo.jpg")
    # Crea video con ffmpeg
    os.system('ffmpeg -y -loop 1 -i output/fondo.jpg -i output/voz.mp3 -c:v libx264 -c:a aac -shortest -vf "scale=1080:1920" output/video_final.mp4')

if __name__ == "__main__":
    tit = buscar()
    print(f"Generando: {tit}")
    asyncio.run(voz(f"{tit}. Mensaje de la estrella del tarot. Sigueme."))
    video(tit)
    print("Video listo")
