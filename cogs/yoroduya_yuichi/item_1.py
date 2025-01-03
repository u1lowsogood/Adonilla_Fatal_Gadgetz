from textwrap import dedent

async def use_item(bot, ctx):
    msg = dedent(f"""
        親愛なる <@216478397570744320> 様へ―――。

        {ctx.author.mention} が
        # __「ゆういちが貴方のことを深く意識する権利」__
        を使用しました！
        彼の祈りに身を捧げましょう……
    """)
    await ctx.send(msg)