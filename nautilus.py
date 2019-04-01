import requests
import discord
import asyncio
import sys
import os
from discord.ext import commands
from datetime    import datetime, timedelta
from operator    import itemgetter
from PIL         import Image, ImageOps, ImageDraw

bot = commands.Bot(command_prefix = '|')

bot.remove_command('help')

def main():
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    stats = {}
    pastWeek = datetime.now() - timedelta(days=int(sys.argv[3]))
    s = None
    for server in bot.servers:
        if server.name == sys.argv[2]:
            s = server
    if s == None:
        print("No server found")
        return

    for channel in s.channels:
        lastMessage = None
        print(channel.name)
        while True:
            size = 0
            async for msg in bot.logs_from(channel, before = lastMessage, limit = 100):
                if msg.timestamp > pastWeek and not msg.author.bot:
                    if msg.author.id in stats:
                        stats[msg.author.id]["msg"] += 1
                    else:
                        url = msg.author.avatar_url.replace("webp", "png")
                        if url != "":
                            stats[msg.author.id] = {"url": url, "msg": 1}
                    size += 1 
                lastMessage = msg
            if size != 100 or (lastMessage != None and msg.timestamp < pastWeek):
                break

    for id in stats.keys():
        print("Dowloading " + id + ".png")
        r = requests.get(stats[id]["url"], allow_redirects=True)
        open("tmp/" + id + ".png", 'wb').write(r.content)

    sortedStats = []
    for id in stats.keys():
        sortedStats.append({"fn": "tmp/" + id + ".png", "msg": stats[id]["msg"]})
    sortedStats = sorted(sortedStats, key=itemgetter('msg'), reverse = True)

    scl = fib(int(sys.argv[4]))
    pos = positions(int(sys.argv[4]))
    background = Image.open(sys.argv[1])

    factor = int((background.height/scl[0]) * 5)
    total = Image.new('RGBA', ((scl[0] + scl[1]) *factor, scl[0] *factor), (255, 0, 0, 0))

    for n in range(0, int(sys.argv[4])):
        profileImage, mask = getProfilePic(sortedStats[n], scl[n]*factor)
        total.paste(profileImage, box=multTuple(pos[n], factor), mask=mask)
    
    total.save("foreground.png", "PNG")

    total.resize((background.size[0], background.size[1]), Image.ANTIALIAS)
    total = scale(background, total, float(sys.argv[5]))
    background.paste(total, (background.width - total.width, 0), total)
    background.save("wallpaper.png", "PNG")

    await bot.logout()

def getProfilePic(user, scale):
    profileImage = Image.open(user["fn"])
    bigsize = (profileImage.size[0] * 3, profileImage.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    profileImage = profileImage.resize((scale, scale))
    mask = mask.resize(profileImage.size, Image.ANTIALIAS)

    return profileImage, mask

def scale(background, total, scl):
    factor = min(background.height / total.height, background.width / total.width)
    return total.resize((int(total.width * factor * scl), int(total.height * factor * scl)))

def fib(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    result = [1, 1]
    if n == 2:
        return result
    for i in range(2, n):
        result.append(result[i-1] + result[i-2])
    result.reverse()
    return result

def positions(val):
    l = fib(val)
    coor = [(0,0)]
    for n in range (1, val, 4):
        coor.append(
            addTuple(
                coor[n-1],
                (l[n-1], 0)
            )
        )
        coor.append(
            addTuple(
                coor[n],
                (l[n+2], l[n])
            )
        )
        coor.append(
            addTuple(
                coor[n-1],
                addTuple(
                    (l[n-1], l[n-1]),
                    (0, -l[n+2])
                )
            )
        )
        coor.append(
            addTuple(
                coor[n-1],
                addTuple(
                    (l[n-1], l[n-1]),
                    (0, -l[n+1])
                )
            )
        )
    return coor

def addTuple(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))

def multTuple(t, f):
    x, y = t
    return (x*f, y*f)

main()
