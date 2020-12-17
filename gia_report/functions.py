from test_aioredis import get_redis


class Data(object):
    """
    BASE
    """

    def generate(self):
        """
        generate the report
        contain several parameters
        """
        pass

    def __calculation(self, *args, **kwargs):
        """get score depending on the right an error """
        pass

    def __score_t(self, *args, **kwargs):
        """get T_score depending on score"""
        pass

    def __level(self, *args, **kwargs):
        """get level depending on T_score"""
        pass

    def __conclusion(self, *args, **kwargs):
        """get conclusion depending on level"""
        pass

    def __gia(self, *args, **kwargs):
        """add instruction for conclusion"""
        pass


class GiaData(Data):
    def __init__(self, stage):
        # 区别综合分值的处理
        if stage != 'average':
            # stage range 20-24
            self.stage = stage['stage']
            # the right number
            self.r_num = stage['stageResult']['right']
            # the error number
            self.e_num = stage['stageResult']['error']

    async def generate(self):
        # range 20 - 24
        if 25 > self.stage >= 20:
            # choose the stage's description
            description = await get_redis('description')
            description = eval(description)[self.stage]
            # return the score
            s_calculation = await self.__calculation()
            # change to t_score
            s_percentage = await self.__score_t(s_calculation)
            # change to level
            s_level = await self.__level(s_percentage)
            # get conclusion
            conclusion = await self.__conclusion(s_level, s_percentage)
            # format result
            result = {
                "score": s_calculation,
                "T_score": s_percentage,
                "level": s_level,
                "conclusion": conclusion['conclusion'],
                "suggest": conclusion['suggest'],
                "description": description,
            }
            return {self.stage: result}, s_calculation

    async def __calculation(self):
        # 替换值并计算结果
        calculation_data = await get_redis('calculation_data')
        # choose the stage's calculation
        calculation_data = eval(calculation_data)[self.stage]
        # calculate
        score = eval(calculation_data.format(correct_count=self.r_num, finish_count=(self.e_num + self.r_num)))
        return score

    async def __score_t(self, s_calculation):
        # 转换成T分数
        score_percentage = await get_redis('score')
        # 得到分数对应转换字典
        score_list = eval(score_percentage)
        # 计算逻辑：小于这个范围的上限，比之前的上限都大，且是符合的值中最小的一个值
        temp = 0
        if 0 < s_calculation < 100:
            for score in score_list:
                if score >= s_calculation > temp:
                    temp = score
            return score_list[temp]
        elif s_calculation <= 0:
            return 1
        elif 100 <= s_calculation:
            return 99

    async def __level(self, s_percentage):
        # change to level
        # get the regular
        score_level = await get_redis('score_to_level')
        s_level_list = eval(score_level)
        # 计算逻辑：小于这个范围的上限，比之前的上限都大，且是符合的值中最小的一个值
        temp = 0
        if 0 < s_percentage < 100:
            for s_level in s_level_list:
                if s_level >= s_percentage > temp:
                    temp = s_level
            return s_level_list[temp]

    async def __conclusion(self, s_level, s_percentage):
        # 根据level选择对应词
        conclusion_data = await get_redis('conclusion')
        # choose the stage's conclusion
        conclusion_data = eval(conclusion_data)[self.stage]
        # choose the level's sentence
        result = conclusion_data[s_level]
        # 替换得分
        result['conclusion'][0] = result['conclusion'][0].format(s_percentage)
        return result

    async def gti_conclusion(self, score):
        # 处理综合分值
        # 需要用到转换成T_score和转换等级的函数
        t_score = await self.__score_t(score)
        level = await self.__level(t_score)
        # 根据对应等级找到对应语料，并替换对应字符
        gti = await get_redis('gti')
        # choose the level's conclusion
        conclusion = eval(gti)[level]
        # 暂放每句话
        sentences = []
        # 替换对应的语料当中的每句话
        for sentence in conclusion['conclusion']:
            sentence = sentence.format('你', t_score)
            sentences.append(sentence)
        conclusion['conclusion'] = sentences
        # format result
        result = {
            "score": score,
            "T_score": t_score,
            "level": level,
            "conclusion": conclusion['conclusion']
        }
        return {"gti": result}
