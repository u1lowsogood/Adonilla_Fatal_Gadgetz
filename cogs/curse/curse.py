from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import dlib
import cv2
import random
import io
import requests
import discord

class eye:
    def __init__(self,img : Image.Image, eye_points):

        self.img = img.copy()
        self.mask = Image.new("L",self.img.size,0)

        eyemask_draw = ImageDraw.Draw(self.mask)

        tupler = lambda points : tuple(tuple(sublist) for sublist in points)
        eyemask_draw.polygon(tupler(eye_points),fill=255)

    def pasteto(self,to : Image.Image, pos: tuple):

        eye_amount = 14
        rotate_deg = 30

        self.img_buffer = self.img.copy()
        self.mask_buffer = self.mask.copy()
        enhancer = ImageEnhance.Contrast(self.img_buffer)
        self.img_buffer  = enhancer.enhance(2.5)

        degree = random.randrange(-rotate_deg,rotate_deg)
        self.rotate(degree)

        dilatelv = random.randrange(1,10,2)
        self.mask_buffer = self.mask_buffer.filter(ImageFilter.MaxFilter(size=dilatelv))

        #mul = random.uniform(0.8,1.4)
        #self.resize(mul)
        
        to.paste(self.img_buffer,(pos[0],pos[1]),self.mask_buffer)

    def rotate(self, degree):
        self.img_buffer = self.img_buffer.rotate(degree)
        self.mask_buffer = self.mask_buffer.rotate(degree)

def blackfiller(img: Image.Image, points):
    mxx,mxy = (max([p[0] for p in points]), max([p[1] for p in points]))
    mix,miy = (min([p[0] for p in points]), min([p[1] for p in points]))

    #ぼかしマスクを作成し、黒い背景画像を合成する
    blurmask = Image.new("L", img.size, color=0)
    draw = ImageDraw.Draw(blurmask)
    draw.ellipse((mix,miy-(mxy-miy),mxx,mxy+(mxy-miy)),fill=255)
    blurmask = blurmask.filter(ImageFilter.GaussianBlur(radius=1.8))

    superblack = Image.new("RGB", img.size, color=0)
    img = Image.composite(superblack, img, blurmask)

    return img

    #def resize(self, mul):
    #    width, height = self.img_buffer.size
    #    self.img_buffer = self.img_buffer.resize((int(width*mul),int(height*mul)))
    #    self.mask_buffer = self.mask_buffer.resize((int(width*mul),int(height*mul)))

def postalization(image : Image.Image, lv):
    image = image.convert("LAB")
    l,a,b = image.split()

    lut = [(i // (256//lv)) * (256 // lv) for i in range(256)]

    l = l.point(lut)

    image = Image.merge("LAB", (l, a, b))
    image = image.convert("RGB")
    return image

def akazome(image : Image.Image):
    image_gray = image.convert("L") #1チャンネルだけにする
    r,g,b = image.split()

    lut = [0 for _ in range(256)]

    g = g.point(lut)
    b = b.point(lut)
    r = image_gray

    image = Image.merge("RGB",(r,g,b))
    return image

def spiker(image : Image.Image):
    image = image.convert("LAB")
    l,a,b = image.split()

    lut = [i%(256//3)*3 for i in range(256)]

    l = l.point(lut)

    image = Image.merge("LAB", (l, a, b))
    image = image.convert("RGB")
    return image


def yellolize(image : Image.Image): #未使用
    image_gray = image.convert("L") #1チャンネルだけにする

    image = image.convert("CMYK")
    c,m,y,k = image.split()

    lut = [i for i in range(256)]
    ylut = [i*(1/2) for i in range(256)]

    c = c.point(lut)
    m = m.point(lut)
    k = k.point(lut)
    y = y.point(ylut)

    image = Image.merge("CMYK",(c,m,y,k))
    return image

def gaussnoise(image : Image.Image, sigma):
    image = np.array(image)

    noise = np.random.normal(0, sigma, image.shape) #生成した値はfloat32

    image = image.astype(np.float32) + noise #imgはおそらくuint8なので、float32に変換してからノイズを加算
    image = np.clip(image, 0, 255).astype(np.uint8) #最小値0, 最大値255に収めた後に値をuint8に直す。

    image = Image.fromarray(image)
    return image

class Curse(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["呪い画像生成","curse"])
    async def terror(self, ctx):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        feched_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if feched_message.attachments == []:
            await ctx.send("返\n信\n# 先のメ\nッセージは画像である必要が……\n # ある")
            return
        
        resp = requests.get(feched_message.attachments[0].url, stream=True).raw
        img = np.asarray(bytearray(resp.read()), dtype="uint8")

        #切り抜き用（元の画像）
        origin_pil = Image.open(io.BytesIO(img))

        #あんまデカすぎる画像処理長なるのでリサいず
        width, height = origin_pil.size

        if max(width, height) > 1000:
            scale = 1000 / float(max(width, height))

            origin_pil = origin_pil.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)

        #顔面検知用
        cv2temp = np.asarray(origin_pil,dtype=np.uint8)
        face_cv2 = cv2.cvtColor(cv2temp, cv2.COLOR_RGB2BGR)

        enhancer = ImageEnhance.Brightness(origin_pil)  
        origin_pil = enhancer.enhance(1.5)

        origin_pil = origin_pil.filter(ImageFilter.GaussianBlur(1.2))

        origin_pil = postalization(origin_pil,10)
        origin_pil = akazome(origin_pil)

        origin_pil = gaussnoise(origin_pil, 20)

        #出力先
        edited_pil = origin_pil.copy()

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("cogs/curse/shape_predictor_68_face_landmarks.dat")

        faces = detector(face_cv2, 1)

        for face in faces:

            landmark = predictor(face_cv2, face)
            shape_2d = np.array([[p.x, p.y] for p in landmark.parts()])

            eye_points = [shape_2d[36:42],shape_2d[42:48]]
            mouth_points = shape_2d[48:68]

            eyes = [eye(origin_pil,eye_points[0]),eye(origin_pil,eye_points[1])]

            #眼球貼り付け先の座標を乱数生成
            for _ in range(14):
                for ey in eyes:
                    pos = (int(np.random.normal(0, 3, 1)[0]*10),int(np.random.normal(0, 3, 1)[0])*20)
                    ey.pasteto(edited_pil,pos)

            edited_pil = blackfiller(edited_pil, eye_points[0])
            edited_pil = blackfiller(edited_pil, eye_points[1])    
            edited_pil = blackfiller(edited_pil, mouth_points)    

        edited_pil = spiker(edited_pil)

        edited_pil.save("cogs/curse/test.png")

        bio = io.BytesIO()
        edited_pil.save(bio, format='PNG')
        fp = io.BytesIO(bio.getvalue())
    
        img_file = discord.File(fp=fp,filename="cursed.png")

        await ctx.send(file=img_file)


async def setup(bot):
    await bot.add_cog(Curse(bot))