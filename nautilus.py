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
    os.chdir(sys.path[0])
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    stats = {} 
    pastTimeStamp = datetime.now() - timedelta(days=int(sys.argv[2]))
    #Get server
    s = None
    for server in bot.guilds:
        if server.name == sys.argv[1]:
            s = server
    if s == None:
        print("No server found")
        await bot.logout()
        return

    #Get server stats
    for channel in s.channels:
        if channel.type == discord.ChannelType.text:
            lastMessage = None
            total = 0
            read = 0
            size = 100
            while size == 100:
                size = 0
                messages = await channel.history(
                        before = lastMessage,
                        limit = 100).flatten()
                for msg in messages:
                    size += 1
                    if msg.created_at > pastTimeStamp and not msg.author.bot:
                        read += 1
                        if msg.author.id in stats:
                            stats[msg.author.id]["msg"] += 1
                        else:
                            stats[msg.author.id] = {
                                "url": str(msg.author.avatar_url_as(format="png")),
                                "msg": 1}            
                    lastMessage = msg
                    if lastMessage != None and msg.created_at < pastTimeStamp:
                        size = 0
                        break
                total += size
            if read > 0:
                print("{0}:\t{1}".format(channel.name, read))

    #Sort server stats
    print("----------------")
    sortedStats = []
    for id in stats.keys():
        sortedStats.append({
            "id": id,
            "url": stats[id]["url"],
            "msg": stats[id]["msg"]})
    sortedStats = sorted(sortedStats, key=itemgetter('msg'), reverse = True)
    print("Individual Users: {}".format(len(sortedStats)))
    print("----------------")
    # get top 8 users
    sortedStats = sortedStats[:8]
    for stat in sortedStats:
        print("{0}:\t{1}".format(
            s.get_member(stat["id"]).display_name,
            stat["msg"]))

    #Dowload Pictures
    print("----------------")
    for stat in sortedStats:
        stat["path"] = f"tmp/{stat['id']}.png"
        print(f'Dowloading {stat["path"]}')
        r = requests.get(stat["url"], allow_redirects=True)
        open(stat["path"], 'wb').write(r.content)

    #Generate Images
    scl, pos = fib(8), positions(8)
    x, y = scl[0] + scl[1], scl[0]
    factor = round((int(sys.argv[3])/x) * 2)
    x, y = x * factor, y * factor
    total = Image.new('RGBA', (x,y) , (0, 0, 0, 0))
    for n in range(0, 8):
        profileImage, mask = getProfilePic(sortedStats[n], scl[n]*factor)
        total.paste(profileImage, box=multTuple(pos[n], factor), mask=mask)
    total.save("foreground.png", "PNG")
    await bot.logout()

def getProfilePic(user, scale):
    profileImage = Image.open(user["path"])
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
#reversed fibonacci sequence
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
                (l[n-1], 0)))
        coor.append(
            addTuple(
                coor[n],
                (l[n+2], l[n])))
        coor.append(
            addTuple(
                coor[n-1],
                addTuple(
                    (l[n-1], l[n-1]),
                    (0, -l[n+2]))))
        coor.append(
            addTuple(
                coor[n-1],
                addTuple(
                    (l[n-1], l[n-1]),
                    (0, -l[n+1]))))
    return coor

def addTuple(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))

def multTuple(t, f):
    x, y = t
    return (x*f, y*f)

main()
