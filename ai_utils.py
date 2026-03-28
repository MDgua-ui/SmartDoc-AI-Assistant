from aip import AipOcr, AipContentCensor, AipNlp
from config import BAIDU_API_KEY, BAIDU_SECRET_KEY

class SmartDocAI:
    def __init__(self):
        # 初始化三大AI客户端
        self.ocr_client = AipOcr(BAIDU_API_KEY, BAIDU_SECRET_KEY)
        self.censor_client = AipContentCensor(BAIDU_API_KEY, BAIDU_SECRET_KEY)
        self.nlp_client = AipNlp(BAIDU_API_KEY, BAIDU_SECRET_KEY)

    # -------------------------- 1. OCR图片文字识别 --------------------------
    def ocr_image(self, image_path=None, image_url=None):
        """识别图片文字：支持本地图片/网络图片"""
        try:
            if image_path:
                with open(image_path, 'rb') as f:
                    image = f.read()
                res = self.ocr_client.basicGeneral(image)
            elif image_url:
                res = self.ocr_client.basicGeneralUrl(image_url)
            else:
                return "未传入图片"

            # 提取识别结果
            words_result = res.get('words_result', [])
            text = "\n".join([item['words'] for item in words_result])
            return text if text else "未识别到文字"
        except Exception as e:
            return f"OCR识别失败：{str(e)}"

    # -------------------------- 2. 文本内容审核 --------------------------
    def text_censor(self, text):
        """检测文本是否包含违规内容"""
        try:
            res = self.censor_client.textCensorUserDefined(text)
            conclusion = res.get('conclusion', '审核失败')
            conclusion_type = res.get('conclusionType', 0)
            # 1：合规 2：违规 3：疑似
            return f"审核结果：{conclusion}（类型：{conclusion_type}）"
        except Exception as e:
            return f"审核失败：{str(e)}"

    # -------------------------- 3. 文本智能摘要 --------------------------
    def text_summary(self, text, max_len=100):
        """长文本自动生成摘要"""
        try:
            res = self.nlp_client.newsSummary(text, max_len)
            return res.get('summary', '摘要生成失败')
        except Exception as e:
            return f"摘要生成失败：{str(e)}"

    # -------------------------- 4. 关键词提取 --------------------------
    def extract_keywords(self, text, top_num=5):
        """提取文本核心关键词"""
        try:
            res = self.nlp_client.keyword(text, top_num)
            keywords = [item['word'] for item in res.get('items', [])]
            return ", ".join(keywords) if keywords else "未提取到关键词"
        except Exception as e:
            return f"关键词提取失败：{str(e)}"

    # -------------------------- 一站式处理 --------------------------
    def full_process(self, image_path=None, image_url=None):
        """一站式：识别+审核+摘要+关键词"""
        print("🔍 开始AI处理...")
        # 1. OCR识别
        ocr_text = self.ocr_image(image_path, image_url)
        print("✅ OCR识别完成")

        if ocr_text.startswith("OCR识别失败") or ocr_text == "未识别到文字":
            return {"识别结果": ocr_text}

        # 2. 内容审核
        censor_res = self.text_censor(ocr_text)
        print("✅ 内容审核完成")

        # 3. 智能摘要
        summary_res = self.text_summary(ocr_text)
        print("✅ 智能摘要完成")

        # 4. 关键词提取
        keywords_res = self.extract_keywords(ocr_text)
        print("✅ 关键词提取完成")

        return {
            "识别文本": ocr_text,
            "内容审核": censor_res,
            "智能摘要": summary_res,
            "核心关键词": keywords_res
        }