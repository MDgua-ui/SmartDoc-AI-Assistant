from ai_utils import SmartDocAI

def save_result(result, filename="AI处理报告.txt"):
    """保存处理结果到本地文件"""
    with open(filename, "w", encoding="utf-8") as f:
        for k, v in result.items():
            f.write(f"【{k}】\n{v}\n\n")
    print(f"\n📄 报告已保存：{filename}")

if __name__ == '__main__':
    # 初始化AI助手
    ai = SmartDocAI()

    # ====================== 使用方式 ======================
    # 方式1：本地图片（替换为你的图片路径）
    result = ai.full_process(image_path="test.jpg")

    # 方式2：网络图片
    # result = ai.full_process(image_url="https://example.com/test.jpg")
    # ======================================================

    # 打印结果
    print("\n" + "="*50)
    for key, value in result.items():
        print(f"【{key}】\n{value}\n")

    # 保存报告
    save_result(result)