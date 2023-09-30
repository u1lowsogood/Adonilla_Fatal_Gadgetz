from discord.ext import commands
import cv2
import numpy
import random
import io
import discord

class Generatemap(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["genm","マップ生成"],description="架空の地図を生成します。第１引数にシードを指定もできます")
    async def generatemap(self, ctx, seedkun:int = None):
        message = ctx.message

        if seedkun == None:
            seedkun = random.randrange(9999999999)

        countrynames = ["ウンコ","乳","アナル開通","直結","脱糞","発狂","キチガイ","デストロイ","煉獄","わんぱく","よろこび","ふわふわ","殺害","圧殺","コンドーム","窒息"
                        "フトマラ","陰毛","セックス","交尾","だいすき","変態","アヘ顔","スカルファック","脱糞","爆","激","最強","ナチ","クソ","デカマラ","天誅","殺すぞ"
                        "フェラチオ","髪コキ","PORNHUB","口コキ","浣腸セックス","斬首","淫行","Footjob","ゲロ","膣圧","下痢","利尿","うれしみ","たのしみ","わくわく","わんぱく"]
        
        countrytypes = ["村","里","連邦","町","街","島","人民共和国","共産国家","社会主義共和国","帝国","王国","公国","大公国","首長国","首長国連邦","共和国","連合"]

        countrydetail_sangyou = ["観光業","農業","紛争","工業","漁業","性風俗","宗教","自動車工業","林業","分業","ビジネス業","情報業","産業","ワイン産業","アグリビジネス","焼き畑農業"]

        countrydetail_riyuu = ["その治安の悪さから","その肥沃な土地から","その広大な土地から","その歴史ある文化から","その犯罪率の高さから","その由緒ある王家から","その洗練された技術力から",
                                "その優れた政治制度から","その高い軍事力から","その枯れた大地から","その情報網の発展から","その優れた福祉厚生から","その税率の高さから","その美しい自然から",
                                "その汚染された大気から","その薄汚れた血筋から","その敗戦後の発展から","その貧富の格差から"]

        countrtydetail_koyuu = ["アナルビーズ","電動バイブ","ピンクローター","極太ディルド","エネマグラ","オナホ","エロVチューバ―","AV（アダルトビデオ）",
                                "イチジク浣腸","貞操帯","コンドーム","ローション","サプリメント","バージンループ","ラブドール","クリバイブ","電マ","吸盤ディルド","馬ディルド","巨大ディルド",
                                "エロASMR","エロ掲示板","膣","チンポ","ヒリたてウンコ","精力剤","FC2","ゲロ","陰毛","ペニバン","肛門開きマシン","アナル拡張機器","巨大アナルビーズ",
                                "浣腸","巨大イチジク浣腸","スカトロAV（アダルトビデオ）","ゲロAV（アダルトビデオ）","乳首開発キット","肛門鏡","性奴隷","肉オナホ","マン毛",
                                "動物姦AV（アダルトビデオ）","脳姦AV（アダルトビデオ）","体液","精子","Xhamster","Redtube","Pornhub"]

        countrydetail_amounts = ["多い","国民の生活を支えている","とても多い","世界のシェアを占める","大半を占めている","トップ３に入る","年に"+str(random.randrange(1000))+"個である"]

        countryname = ""
        countrytype = random.choice(countrytypes)

        for i in range(random.randint(1,3)):
            countryname = countryname + random.choice(countrynames)
        countryname = countryname + countrytype

        countryexplanations = [
        countryname + "では" +random.choice(countrydetail_sangyou) + "が盛んであり、"+random.choice(countrtydetail_koyuu)+"の生産が"+random.choice(countrydetail_amounts)+"。\n",
        "この"+countrytype+"は、主に"+random.choice(countrydetail_riyuu)+random.choice(countrtydetail_koyuu)+"によって知られている。\n",
        random.choice(countrydetail_sangyou)+"を生かした地形がとても有名。\n",
        "この"+countrytype+"の名前は、"+random.choice(countrydetail_riyuu)+"名付けられた。\n",
        "この"+countrytype+"の歴史は深く、"+random.choice(countrtydetail_koyuu)+"の文化が根強く残っている。\n",
        random.choice(countrydetail_sangyou)+"の文化は、"+random.choice(countrydetail_riyuu)+"影響を受けている。\n",
        "食べ物としては" + random.choice(countrtydetail_koyuu) + "が大変有名である。\n" ,
        "動物たちは"+random.choice(countrydetail_riyuu)+"、" + random.choice(countrtydetail_koyuu)+"を求めて"+random.choice(countrydetail_sangyou)+"の人々と触れ合う。\n"]

        countryexplanation = "国名：" + countryname + "\n\n国土面積："+str(random.randrange(9999999))+"km²\n人口："+str(random.randrange(999999999))+"万人\n国内総生産："+str(random.randrange(9999999))+"兆アメリカ合衆国ドル (2018年)\n平均寿命："+str(random.randrange(110))+"歳\n\n説明：\n"

        howmuch = random.randint(2,3)
        l = random.sample(countryexplanations,howmuch)

        for i in range(howmuch):
            
            if i == 1:
                countryexplanation = countryexplanation + "また、"
            elif i == 2:
                countryexplanation = countryexplanation + "そして、"
            elif i == 3:
                countryexplanation = countryexplanation + "さらに、"

            countryexplanation = countryexplanation + l[i]

        mapx = 500
        mapy = 500

        sea = numpy.zeros((mapy, mapx, 3))
        sea += [0,random.randint(0,255),random.randint(150,255)][::-1] 

        pins = [
            [(1,0),(2,0),(3,0),(4,1),(4,2),(4,3),(3,4),(2,4),(1,4),(0,3),(0,2)],#ラウンド型
            [(3,4),(4,4),(4,3),(3,3),(3,2),(3,1),(3,0),(2,0),(2,1),(2,2),(2,3),(1,3),(1,4),(2,4)],#ちんこ
            [(2,4),(3,3),(4,2),(3,1),(2,0),(1,1),(0,2),(1,3),(2,4)],#だいあ
            [(1,3),(2,3),(3,3),(3,2),(3,1),(2,1),(1,1),(1,2)],#中
            [(3,3),(3,2),(2,2),(2,3)],#小さい
            [(4,4),(4,3),(3,2),(3,1),(4,0),(3,0),(2,1),(1,1),(0,0),(0,1),(1,2),(1,3),(0,4),(1,4),(2,3),(3,3)],#謎卍
            [(2,1),(1,2),(0,2),(0,3),(0,4),(1,4),(2,4),(2,3),(3,2),(4,2),(4,1),(4,0),(3,0),(2,0)],#クリープ
            [(3,1),(4,1),(4,0),(3,0),(2,0),(2,1),(1,1),(1,0),(0,0),(0,1),(0,2),(1,2),(1,3),(0,3),(0,4),(1,4),(2,4),(2,3),(3,3),(3,4),(4,4),(4,3),(4,2),(3,2)],#ナチス
            [(3,3),(4,3),(4,2),(4,1),(3,2),(3,1),(3,0),(2,0),(2,1),(1,1),(1,2),(0,2),(0,3),(1,3),(1,4),(2,4),(2,3)],#わからん
            ]

        zure = [random.randint(30,50),random.randint(10,40),random.randint(5,20),random.randint(0,10),random.randint(0,5),4,3,2]
        points = []
        chutens = []

        areasize = 100

        for pin in pins[random.randrange(len(pins))]:
            points.append((random.randrange(areasize)+pin[0]*areasize,random.randrange(areasize)+pin[1]*areasize))

        for k in range(6):
            for i in range(len(points)):
                if i < len(points)-1:
                    chutens.append((round((points[i][0]+points[i+1][0])/2)+random.randint(-zure[k],zure[k]),round((points[i][1]+points[i+1][1])/2)+random.randint(-zure[k],zure[k])))
                else:
                    chutens.append((round((points[i][0]+points[0][0])/2)+random.randint(-zure[k],zure[k]),round((points[i][1]+points[0][1])/2)+random.randint(-zure[k],zure[k])))

            result = [None]*(len(points)+len(chutens))
            result[::2] = points
            result[1::2] = chutens

            points = result
            chutens = []

        worldcolors = [[0,random.randint(60,255),random.randint(0,80)][::-1] ,[random.randint(170,210),random.randint(140,200),0][::-1]]

        cv2.fillPoly(sea, [numpy.array(points)], worldcolors[random.randint(0,1)])

        cv2.putText(sea,  "seed: " + str(seedkun), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 0), lineType=cv2.LINE_AA)

        img_bytes = cv2.imencode('.png', sea)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="map.png")

        await message.channel.send(file=img_file)
        await message.channel.send(countryexplanation)

async def setup(bot):
    await bot.add_cog(Generatemap(bot))