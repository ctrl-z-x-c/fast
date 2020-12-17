from .functions import GiaData


async def loop(stagedata):
    # get 5 kinds of score
    result_dict = {}
    # get average ready for gti
    sum_score = 0
    # every stage makes a result
    for stage_i in stagedata.stageData:
        result, return_score = await GiaData(stage_i).generate()
        sum_score += return_score
        result_dict.update(result)
    # get average
    average_score = sum_score / 5
    # 单独的函数对gti做出计算
    result = await GiaData('average').gti_conclusion(average_score)
    result_dict.update(result)
    return result_dict
