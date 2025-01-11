from textwrap import dedent

async def use_item(bot, ctx):
    msg = dedent(f"""
        おい、 <@216478397570744320> ！

        {ctx.author.mention} が
        # __「ゆういちがシコティッシュを晒す権利」__
        を使用しました！
        ※写真を撮るので時間がかかる場合がございます。
    """)
    await ctx.send(msg)