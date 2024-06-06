import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()
async def requestTo(body,size,scale,chatid,userid):

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:5000',json = {'body':body,'size':size,'scale':scale,'chatid':chatid,'userid':userid}) as response:
            return 'ok'
