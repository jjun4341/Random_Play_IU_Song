import discord
import wavelink
from discord.ext import commands
import random

class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=['!'])

        self.add_cog(Music(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='1oveIU',
                                              identifier='IU_Random_Play',
                                              region='us_central')

    @commands.command(name = '뽑기')
    async def play(self, ctx):

        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send('먼저 음성 채널에 접속해주세요!')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)
        await ctx.send(f'`{channel.name}`에 연결합니다.')

        await ctx.send('IU 노래를 랜덤으로 뽑는 중입니다..')

        random_song = ['Celebrity', 'eight', 'blueming', 'bbibbi', '내 손을 잡아', '이 지금', '밤편지', '팔레트', '좋은날', '너랑 나', 'into the I-LAND', '이런 엔딩', '시간의 바깥', '마음을 드려요', 'love poem', '분홍신', '너의 의미', '이름에게', '스물셋', '봄 사랑 벚꽃 말고', '금요일에 만나요', 'SOMEDAY', '사랑이 잘', '가을 아침', '잼잼', '잔소리', '나의 옛날이야기', 'Uaena', '하루 끝', '미리 메리 크리스마스', '이지금', 'Rain Drop']
        random_song = random.choice(random_song)
        query = 'iu' + random_song
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('아쉽지만 유튜브에서 곡을 찾지 못했어요. :cry: ')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.send(':no_entry_sign: 음성 채널에 접속하고 이 명령어를 사용해주세요.')
        await ctx.send(f'`{random_song}` 곡을 재생할게요!')
        await player.play(tracks[0])


bot = Bot()
bot.run('TOKEN')