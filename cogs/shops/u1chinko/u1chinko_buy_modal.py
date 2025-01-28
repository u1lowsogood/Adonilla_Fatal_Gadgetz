import discord
from discord import ui

class U1Chinko_Buy_Modal(ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(ui.Select(placeholder="購入するアイテムを選択"))
        self.add_item(ui.TextInput(label="名前", placeholder="例：太郎"))
        self.add_item(ui.TextInput(label="年齢", placeholder="例：20", min_length=1, max_length=2, required=True))

    async def callback(self, interaction: discord.Interaction):
        name = self.children[0].value
        age = self.children[1].value
        await interaction.response.send_message(f"こんにちは、{name}さん！ あなたは{age}歳ですね。")

    @bot.tree.command(name="textinput", description="テスト")
    async def textinput_command(interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal(title="情報を入力してください"))