import os
from text_extractor.T_pre_processor import TPreProcessor
from text_extractor.sentence_positioner import Sentence_Positioner
from text_extractor.Phrase_parse import Phrase_parse
from text_extractor.Relation_extraciton import Relation_extraciton

# 1. 基础配置
# 假设你刚刚生成的txt文件名为 paper_output.txt
txt_file_path = "paper_output.txt" 
# 项目中的字典配置文件路径（必须确保在你的项目目录下存在此文件）
c_path = r".\pipeline\dictionary.ini" 
# 目标属性：根据论文，主要性能为硬度（Vickers hardness, HV）
prop_name = "hardness" 

print(f"开始提取目标属性: {prop_name}...\n" + "-"*50)

# 2. 读取文本并进行预处理
with open(txt_file_path, 'r', encoding='utf-8') as file:
    data = file.read()

processor = TPreProcessor(data, prop_name, c_path)
filter_txt = processor.processor()

# 3. 句子分类：找出所有包含“硬度”信息的句子
positioner = Sentence_Positioner(filter_txt, prop_name, c_path)
target_sents = positioner.target_sent()

print(f"共找到 {len(target_sents)} 个包含目标属性的句子。\n" + "-"*50)

# 4. 命名实体识别与关系抽取（遍历每个句子）
for n, sent in target_sents.items():
    print(f"【原文句子】: {sent}")
    
    # 解析短语结构
    parse = Phrase_parse(sent, prop_name, c_path)
    sub_order, sub_id, object_list = parse.alloy_sub_search()
    
    print(f" -> 识别到的合金名称: {sub_order}")
    print(f" -> 识别到的参数数值: {object_list}")
    
    # 抽取三元组关系
    RE = Relation_extraciton(prop_name, sent, sub_order, sub_id, object_list, c_path)
    all_outcome = RE.triple_extraction()
    
    print(f" -> 最终关系抽取结果: {all_outcome}\n")