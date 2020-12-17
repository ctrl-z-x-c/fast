import asyncio
import aioredis
import gia_attribute


# 设置redis数据
async def set_redis(r_key, r_value):
    redis = await aioredis.create_redis_pool('redis://localhost')
    await redis.set(r_key, r_value)
    redis.close()
    await redis.wait_closed()


# 读取redis数据
async def get_redis(r_key):
    redis = await aioredis.create_redis_pool('redis://localhost')
    value = await redis.get(r_key, encoding='utf-8')
    redis.close()
    await redis.wait_closed()
    return value







if __name__ == '__main__':
    # deal with the calculation
    calcu_data = gia_attribute.GIA_CALCULATION
    # deal with the T_score
    t_scores = gia_attribute.GIA_SCORE_T
    # deal with the T_score to level
    score_levels = gia_attribute.GIA_LEVEL_SUMMARY
    # deal with conclusion
    conclu_data = gia_attribute.GIA_LEVEL_CONCLUSION
    # deal with description
    gia_des = gia_attribute.GIA_DESCRIPTION
    # gia
    gti_detail = gia_attribute.GIA_GTI

    # 计算方式
    # 分数百分转换
    # change t_score to level
    # get conclusion
    # add description
    # gti
    asyncio.run(set_redis('calculation_data', str(calcu_data)))
    asyncio.run(set_redis('score', str(t_scores)))
    asyncio.run(set_redis('score_to_level', str(score_levels)))
    asyncio.run(set_redis('conclusion', str(conclu_data)))
    asyncio.run(set_redis('description', str(gia_des)))
    asyncio.run(set_redis('gti', str(gti_detail)))

