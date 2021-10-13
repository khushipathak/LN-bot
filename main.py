import keep_alive

from discord.ext import commands
import discord
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

client = discord.Client()


def makeID(id, name, join):

    id_card = Image.open("id_temp.png")

    av = Image.open("user-av.png")
    width, height = av.size

    av = av.resize((150, 150))
    id_card.paste(av, (70, 280))

    nametext = ImageDraw.Draw(id_card)
    myFont = ImageFont.truetype("Avenir-Medium.ttf", 35)
    nametext.text((70, 490), name.upper(), font=myFont, fill=(252, 230, 215))

    datetext = ImageDraw.Draw(id_card)
    myFont = ImageFont.truetype("Avenir-Medium.ttf", 21)
    datetext.text((69, 200), join, font=myFont, fill=(232, 230, 204))

    idtext = ImageDraw.Draw(id_card)
    myFont = ImageFont.truetype("Avenir-Light.ttf", 35)
    idtext.text((70, 530), id, font=myFont, fill=(137, 135, 117))

    id_card.save("custom_card.png")

    return

def writetissue(msg):

  msg = "\n".join(textwrap.wrap(msg, width=30))

  tis = Image.open("tissue.png")

  msgtis = ImageDraw.Draw(tis)
  myFont = ImageFont.truetype("NothingYouCouldDo.ttf", 35)
  msgtis.multiline_text((250,275), msg, font = myFont, fill=(0,0,0))

  tis.save("custom_tissue.png")

  return


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$id'):
        userid = str(message.author.name) + "#" + str(
            message.author.discriminator)

        name = str(message.author.nick)
        if name == "None":
            name = str(message.author.name)

        joindate = str(message.author.joined_at)[:10]

        await message.author.avatar_url.save("user-av.png")

        makeID(userid, name, joindate)

        card = discord.File("custom_card.png")
        await message.channel.send(file=card,
                                   content="Membership Card: ",
                                   reference=message,
                                   mention_author=True)

    if message.content.startswith('$tissue'):

        name = str(message.author.nick)
        if name == "None":
            name = str(message.author.name)

        user = message.mentions
        if not user:
            await message.channel.send(
                "You forgot to tag the receiver! Type $tissue @receiver <message>"
            )

        else:
            user = message.mentions[0]
            m = " ".join(message.content.split()[2:])

            if not m:
                await message.channel.send(
                    "You forgot to write a message! Type $tissue @receiver <message>"
                )

            else:
                writetissue(m)

                tissue = discord.File("custom_tissue.png")
                await message.channel.send(
                    file=tissue,
                    content="{} has a message for {}!".format(
                        message.author.mention, user.mention))


keep_alive.keep_alive()

client.run(os.getenv('TOKEN'))
