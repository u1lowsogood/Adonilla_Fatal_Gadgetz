from discord.ext import commands
import random

class Itemfusion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.words = [
                 ["クレヤ","ボヤンス"],
                 ["悪魔","の抱擁"],
                 ["ライアンドリー","の苦悶"],
                 ["インフィニティ","エッジ"],
                 ["アビサル","マスク"],
                 ["イージス","の盾"],
                 ["アナセマ","チェイン"],
                 ["アークエンジェル","スタッフ"],
                 ["アクシオム","アーク"],
                 ["バンドルグラス","の鏡"],
                 ["バンシー","ヴェール"],
                 ["ブラック","クリーバー"],
                 ["コールフィールド","ウォーハンマー"],
                 ["ケミパンク","チェーンソード"],
                 ["ケミテック","ピュートリファイアー"],
                 ["コズミック","ドライブ"],
                 ["シャッタードクイーン","クラウン"],
                 ["デス","ダンス"],
                 ["ディヴァイン","サンダラー"],
                 ["ドラクサー","ダスクブレード"],
                 ["赤月","の刃"],
                 ["エッセンス","リーバー"],
                 ["イーブン","シュラウド"],
                 ["エバー","フロスト"],
                 ["フィンブル","ウィンター"],
                 ["フローズン","ハート"],
                 ["ガーゴイル","ストーンプレート"],
                 ["ゴア","ドリンカー"],
                 ["心","の鋼"],
                 ["ヘクステック","ロケットベルト"],
                 ["ホライゾン","フォーカス"],
                 ["アイスボーン","ガントレット"],
                 ["変幻自在","のジャック・ショー"],
                 ["騎士","の誓い"],
                 ["リッチ","ベイン"],
                 ["ソラリ","のロケット"],
                 ["ルーデン","テンペスト"],
                 ["マナ","ムネ"],
                 ["ムーンストーン","の再生"],
                 ["ナッシャー","トゥース"],
                 ["ナヴォリ","クイックブレード"],
                 ["ナイト","ハーベスター"],
                 ["プローラー","クロー"],
                 ["レディアント","ヴァーチュ"],
                 ["ラヴァナス","ハイドラ"],
                 ["リフト","メーカー"],
                 ["ロッド オブ ","エイジス"],
                 ["セラフ","エンブレイス"],
                 ["セルリダ","の怨恨"],
                 ["シュレリア","の戦歌"],
                 ["ショウジン","の矛"],
                 ["スピリット","ビサージュ"],
                 ["ストライド","ブレイカー"],
                 ["トリニティ","フォース"],
                 ["ターボ","ケミタンク"],
                 ["アンブラル","グレイブ"],
                 ["ビジラント","ワードストーン"],
                 ["冬","の訪れ"],
                 ["妖夢","の霊剣"],
                 ["ジーク","コンバージェンス"],
                 ["ゾーニャ","の砂時計"],
                 ["アナセマ","チェイン"],
                 ["始まり","のストップウォッチ"],
                 ["エバー","フロスト"],
                 ["ヘラルド","の瞳"],
                 ["ファーサイト","オルタネーション"],
                 ["ゲイル","フォース"],
                 ["ミカエル","の祝福"],
                 ["オラクル","レンズ"],
                 ["詰め替え","ポーション"],
                 ["シルバーミア","の夜明け"],
                 ["鋼","のショルダーガード"],
                 ["ミニオン","吸収装置"],
                 ["コントロール","ワード"],
                 ["コラプト","ポーション"],
                 ["ラース","エリクサー"],
                 ["霊者","の鎌"],
                 ["レリック","シールド"],
                 ["リーライ クリスタル ","セプター"],
                 ["ステラック","の籠手"]]
        
        self.messages = ["LoLに新アイテムが実装！？",
                    "今メタのアイテムはこれだ！",
                    "OPアイテムすぎるｗ",
                    "アイテム合成してみた！",
                    "新チャンプのアビリティでアイテム合成！",
                    "Riotから新アイテムがリーク！",
                    "新アイテム情報まとめ2023",
                    "こんなアイテムがあったの、知っていましたか？",
                    "昔のバージョンにはこんなアイテムがあったらしい",
                    "新アイテム強すぎｗｗｗ",
                    "LoLがバグった！",
                    "新ビルド必須アイテム！",
                    "そのキャラはこのアイテム積むといいよ"]

    @commands.command(aliases=["アイテム合成","アイテムヒュージョン","if"])
    async def itemfusion(self, ctx):
                 
        pick = random.sample(self.words,2)

        kaminoku = pick[0][0]
        simonoku = pick[1][1]

        if not simonoku.startswith("の"):
            simonoku = " " + simonoku

        await ctx.send(random.choice(self.messages) + "\n# " + kaminoku + simonoku)

    @commands.command(aliases=["超アイテム合成","uif"])
    async def ultimateitemfusion(self,ctx,nagasa : int = random.randint(3,5)):
        if nagasa > len(self.words):
            nagasa = len(self.words)
        elif nagasa <= 2:
            await ctx.send("length must 上回る ２")
            return

        pick = random.sample(self.words,nagasa)

        sendarg = random.choice(self.messages) + "\n# "
        for i, word in enumerate(pick):
            if i == 0: #最初の１個は上の句から始まる
                sendarg += word[0]
                continue
            if i+1 > nagasa-1: #最後の１個は下の句で終わるので中断
                break

            ku = random.randint(0,1) #0:上の句 1:下の句 ランダムで選ぶ

            if len(sendarg)+len(word[ku]) > 2000: #２０００字を超えた場合はそのまま送信
                await ctx.send(sendarg)
                return
            
            sendarg += word[ku]
        sendarg += pick[-1][1] #最後の下の句で終わる

        await ctx.send(sendarg)

async def setup(bot):
    await bot.add_cog(Itemfusion(bot))