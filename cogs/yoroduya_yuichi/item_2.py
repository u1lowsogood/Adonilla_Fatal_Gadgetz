
from textwrap import dedent

async def use_item(bot, ctx):
    msg = dedent(f"""
        ウッス！ <@216478397570744320> クン！ｗ。
    
        {ctx.author.mention} が
        # __「ゆういちが貴方のことを浅く意識する権利」__
        を使用しました！
        オイ！俺のこと考えろ！ｗ
    """)
    await ctx.send(msg)