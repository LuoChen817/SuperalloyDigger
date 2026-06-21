import json

def json_to_markdown(input_file, output_file):
    # 读取 JSON 数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 按页面 ID 排序，如果同一页，则按纵坐标 (bbox[1]) 排序
    data.sort(key=lambda x: (x.get('page_id', 0), x.get('bbox', [0, 0, 0, 0])[1]))

    md_content = []
    
    for item in data:
        content_type = item.get('type')
        content = item.get('content', '').strip()
        
        if not content:
            continue

        if content_type == 'doc_title':
            md_content.append(f"# {content}\n")
        
        elif content_type == 'paragraph_title':
            # 自动处理层级，通常 1. Introduction 是二级标题
            md_content.append(f"## {content}\n")
            
        elif content_type == 'abstract':
            md_content.append(f"> **ABSTRACT**\n>\n> {content}\n")
            
        elif content_type == 'text':
            # 过滤掉页码等页脚干扰信息（简单正则或长度判断）
            if len(content) > 5: 
                md_content.append(f"{content}\n")
                
        elif content_type == 'image' or content_type == 'chart':
            # 提取图表中的描述文字
            md_content.append(f"\n> [图表/图片内容]: {content[:100]}...\n")
            
        elif content_type == 'figure_title':
            md_content.append(f"\n**{content}**\n")
            
        elif content_type == 'table':
            # 如果是 HTML 格式表格，直接放入（MD支持HTML表格）
            md_content.append(f"\n{content}\n")
            
        elif content_type == 'formula':
            # 将公式包裹在 LaTeX 环境中
            md_content.append(f"\n$${content.replace('$', '')}$$\n")
            
        elif content_type == 'reference':
            md_content.append(f"- {content}")

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))

    print(f"转换完成！文件已保存至: {output_file}")

# 使用方法
json_to_markdown('A machine learning-based alloy design system to facilitate the rational design of high entropy alloys with enhanced hardness.json', 'paper_output.md')