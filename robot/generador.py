import os, feedparser, asyncio, edge_tts
from PIL import Image, ImageDraw, ImageFont
import textwrap

def buscar():
    try:
        f = feedparser.parse("https://www.listindiario.com/rss/portada")
        if f.entries:
            return f.entries[0].title
    except: pass
    return "Mensaje de la estrella del tarot"

async def voz(t):
    os.makedirs("output", exist_ok=True)
    c = edge_tts.Communicate(t, "es-DO-JoseManuelNeural", rate="-8%", pitch="-15Hz")
    await c.save("output/voz.mp3")

def video(t):
    img = Image.new('RGB', (1080,1920), (10,10,30))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
    except:
        font = ImageFont.load_default()
    y = 600
    for lin in textwrap.wrap(t.upper(), 22):
        d.text((70,y), lin, font=font, fill=(255,255,255))
        y += 95
    img.save("output/fondo.jpg")
    os.system('ffmpeg -y -loop 1 -i output/fondo.jpg -i output/voz.mp3 -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest -vf "scale=1080:1920,format=yuv420p" output/video_final.mp4')

if __name__ == "__main__":
    tit = buscar()
    asyncio.run(voz(f"{tit}. Mensaje de la estrella del tarot. Sigueme."))
    video(tit)
