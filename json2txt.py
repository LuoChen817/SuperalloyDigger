import json

def json_to_txt(input_json_path, output_txt_path):
    # 1. 加载 JSON 数据
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. 核心逻辑：排序
    # 论文 JSON 通常是分块存储的，必须先按 page_id 排序，同一页内按 y 坐标（bbox[1]）排序
    data.sort(key=lambda x: (x.get('page_id', 0), x.get('bbox', [0, 0, 0, 0])[1]))

    # 3. 提取与过滤
    txt_lines = []
    
    # 定义需要排除的类型（如页眉页脚、页码等，可根据需要增删）
    exclude_types = {'header', 'footer', 'number', 'image'}

    for item in data:
        content_type = item.get('type')
        content = item.get('content', '').strip()

        # 跳过空内容和不需要的类型
        if not content or content_type in exclude_types:
            continue

        # 根据类型添加一些格式化引导
        if content_type == 'doc_title':
            txt_lines.append(f"Title: {content}\n")
        elif content_type == 'paragraph_title':
            txt_lines.append(f"\n{content}")
        elif content_type == 'abstract':
            txt_lines.append(f"Abstract: {content}\n")
        elif content_type == 'table':
            # 简单处理 HTML 表格内容，去除部分标签或直接保留
            txt_lines.append(f"\n[Table Data]:\n{content}\n")
        else:
            # 普通文本（text/reference/formula 等）
            txt_lines.append(content)

    # 4. 写入 TXT 文件
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(txt_lines))

    print(f"成功！TXT 文件已保存至: {output_txt_path}")

# 执行转换
json_to_txt('A machine learning-based alloy design system to facilitate the rational design of high entropy alloys with enhanced hardness.json', 'paper_output.txt')