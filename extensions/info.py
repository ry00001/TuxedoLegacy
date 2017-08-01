import math
import os
import cpuinfo
import discord
from discord.ext import commands
import psutil


def propcheck(prop, d):
    return d[prop] if d[prop] else "None"

class Info:
    def __init__(self, bot):
        self.bot = bot

    def humanbytes(self, B):
        'Return the given bytes as a human friendly KB, MB, GB, or TB string'
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B/KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B/MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B/GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B/TB)

    @commands.command(aliases=["stats"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        """Information!"""
        percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        currproc = psutil.Process(os.getpid())
        print(mem)
        total_ram = self.humanbytes(mem[0])
        available_ram = self.humanbytes(mem[1])
        usage = self.humanbytes(currproc.memory_info().rss)
        cpu_info = cpuinfo.get_cpu_info()
        e = discord.Embed(title="Statistics")
        e.add_field(name="CPU Usage", value=f"**{math.floor(percent)}**%")
        e.add_field(name="RAM Usage", value=f"Total: **{total_ram}**\nAvailable: **{available_ram}**\nUsed by bot: **{usage}**")
        e.add_field(name="Guilds", value=f"{len(self.bot.guilds)}")
        # e.add_field(name="CPU Information", value=f"Vendor: **{propcheck("vendor_id", cpu_info)}**\nBrand: **{propcheck("brand", cpu_info)}** @ **{propcheck("hz_actual", cpu_info)}** (Advertised: {propcheck("hz_advertised", cpu_info)})")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Info(bot))
