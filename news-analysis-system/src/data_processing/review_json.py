import json
"""
检查json文件的内容，查看是哪一条有问题
"""
json_file = '../../data/backup_results/xxxx.json'

with open(json_file, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

print(f"总共有 {len(raw_data)} 条记录")

for i, item in enumerate(raw_data):
    try:
        obj = json.loads(item)
    except json.JSONDecodeError as e:
        print(f"\n❌ 第 {i} 条 JSON 解析失败:")
        print(f"错误信息: {e}")
        print(f"内容:\n{item}")
        break
