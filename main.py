import os
import discord
from discord.ext import commands
from discord import app_commands
from alive import server_on

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# กำหนด prefix สำหรับบอท
bot = commands.Bot(command_prefix='!', intents=intents)

class MyModal(discord.ui.Modal, title='Login auto check in Hoyoverse Games'):
    UID = discord.ui.TextInput(label='UID', placeholder='Enter your uid game', required=True)
    GAME = discord.ui.TextInput(label='The game you will log in to', placeholder='Genshin , Starrail , zzz , honkai3 ', required=False)
    TOKEN  = discord.ui.TextInput(label='TOKEN', placeholder='Enter your token', required=False)
    ltuid  = discord.ui.TextInput(label='ltuid', placeholder='Enter your ltuid', required=False)



    async def on_submit(self, interaction: discord.Interaction):
        # ID ของช่องแชทที่ต้องการส่งข้อมูลไป
        target_channel_id = 1277786319195734132  # แทนที่ด้วย ID ของช่องแชทที่ต้องการส่งข้อความไป
        
        # ค้นหาช่องแชทตาม ID
        target_channel = bot.get_channel(target_channel_id)
        if target_channel:
            # สร้าง Embed
            embed = discord.Embed(title='Login submit auto login', color=discord.Color.blue())
            embed.add_field(name=' Submitted By', value=f'<@{interaction.user.id}>', inline=False)
            embed.add_field(name='UID', value=f'`{self.UID.value}`', inline=False)
            embed.add_field(name='GAME', value=f'`{self.GAME.value}`', inline=False)
            embed.add_field(name='TOKEN', value=f'`{self.TOKEN.value}`', inline=False)
            embed.add_field(name='ltuid', value=f'`{self.ltuid.value}`', inline=False)

            # ส่ง Embed ไปยังช่องแชทที่กำหนด
            await target_channel.send(embed=embed)
        else:
            await interaction.response.send_message("Channel not found.", ephemeral=True)

        # ตอบกลับผู้ใช้ที่ส่ง Modal
        await interaction.response.send_message('Your data has been sent!', ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print (f'Logged in as {bot.user}')
    
    # Setting the bot's streaming activity
    streaming_activity = discord.Streaming(
        name="Dev by Nattapat2871",
        url="https://www.twitch.tv/nattapat2871_"
    )
    await bot.change_presence(activity=streaming_activity)

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # แปลงเป็น milliseconds
    await ctx.send(f'Pong! {latency:.2f}ms')

@bot.tree.command(name='ping',description='ping bot')
async def ping(ctx):
    latency = bot.latency * 1000  # แปลงเป็น milliseconds
    await ctx.send(f'Pong! {latency:.2f}ms')

# กรณีใช้ app_commands:
@bot.tree.command(name='login', description='login auto checkin hoyoverse games')
async def login(interaction: discord.Interaction):
    modal = MyModal()
    await interaction.response.send_modal(modal)

@bot.command()
async def login(ctx):
    modal = MyModal()
    await ctx.send_modal(modal)

@bot.tree.command(name="help", description="แสดงคำสั่งช่วยเหลือ")
async def help_command(interaction: discord.Interaction):
    # ส่งการตอบกลับแบบโต้ตอบเพื่อแจ้งให้ Discord ทราบว่าคุณกำลังดำเนินการ
    await interaction.response.defer()

    # สร้าง Embed ขึ้นมา
    embed = discord.Embed(
        title="ช่วยเหลือ",
        description="นี่คือคำแนะนำเกี่ยวกับการใช้งาน bot",
        color=discord.Color.blue()
    )

    # เพิ่มลิงก์ YouTube เข้าไปใน Embed
    embed.add_field(
        name="",
        value="[ดิสเจ้าของบอท](https://discord.com/users/1007237437627572275)",
        inline=False
    )

    # ส่ง Embed
    await interaction.followup.send(embed=embed)

    # ส่งข้อความธรรมดานอกเหนือจาก Embed
    await interaction.followup.send("https://www.youtube.com/watch?v=UN29g2G7RsA")



SOURCE_CHANNEL_ID = 1277720004166680596  # แทนที่ด้วย ID ของช่องแชทต้นทาง
TARGET_CHANNEL_ID = 1269296804688826479  # แทนที่ด้วย ID ของช่องแชทปลายทาง

@bot.event
async def on_message(message):
    # ตรวจสอบว่าข้อความมาจากช่องต้นทางและมาจาก webhook
    if message.channel.id == SOURCE_CHANNEL_ID and message.webhook_id:
        for embed in message.embeds:  # ดึงข้อมูล embed จากข้อความ
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            await target_channel.send(embed=embed)

    await bot.process_commands(message)

server_on()

# ใส่โทเค็นของบอท
bot.run(os.getenv('TOKEN'))
