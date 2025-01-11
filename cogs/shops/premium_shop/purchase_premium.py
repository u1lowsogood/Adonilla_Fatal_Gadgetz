from textwrap import dedent

async def use_item(bot, ctx, role_id):
    role = ctx.guild.get_role(role_id[1])
    member = ctx.author
    if role:
        await member.add_roles(role)
        await ctx.send(f'{member.mention} に <@&{role_id[0]}> を付与しました！')
    else:
        await ctx.send('指定されたIDの役職が見つかりません！')