from textwrap import dedent

async def use_item(bot, ctx):
    msg = dedent(f"""
        親愛なる <@216478397570744320> 様へ―――。

        {ctx.author.mention} が
        # __「ゆういちが貴方に絵を描く権利」__
        を使用しました！
        彼の神技を、その目でご照覧あれ―――！
    """)
    await ctx.send(msg)