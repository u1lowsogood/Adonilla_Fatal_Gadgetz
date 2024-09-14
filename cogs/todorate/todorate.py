from discord.ext import commands
import random

class Todorate(commands.Cog):
    @commands.command(aliases=["2dr"])
    async def todorate(self, ctx):

        cmd = ctx.message

        targetmsg = await cmd.channel.fetch_message(cmd.reference.message_id)
        targetmsg_content = targetmsg.content
        
        bunbo = sum(r=="+" or r=="-" for r in targetmsg_content.split())
        bunshi = sum(r=="+" for r in targetmsg_content.split())
    
        if cmd.reference == None:
            await cmd.channel.send("このコマンドは返信内で使用してね（右クリック → 返信）")
            return
        if bunbo == 0:
            kaisetu = "diff形式で書かれたToDoリストに対して使ってね\n"
            kaisetu += "解説\ndiff形式で記述されたものの達成率を表示する\n\n【diff is 何】\n```diff\n+ 起床する\n- シャワーを浴びる\n```\n↑この形式のこと"
            kaisetu += "かきかた：\n\`\`\`diff\n内容\n\- 未達成事項\n+ 達成事項\n\`\`\`\n（本来はgitとかで追記された内容を表示するもの）"
            await cmd.channel.send(kaisetu)
            return

        sendmsg = "**```md\n# 今日のコンプリート率は...\n```**\n"
        sendmsg += "".join(f"# {round((bunshi/bunbo)*100,2)}％\n")
        sendmsg += "|" + "".join(["-" for _ in range(bunshi-1)])+"🤓"+"".join(["-" for _ in range(bunbo-bunshi)]) + f"| ({bunshi}/{bunbo})\n\n"
        sendmsg += "```md\n# よかったね\n```"

        await ctx.send(sendmsg)

async def setup(bot):
    await bot.add_cog(Todorate(bot))