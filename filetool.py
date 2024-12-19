import os

from pdf2docx import Converter
from docx2pdf import convert
import pandas as pd


def process_file(filepath):
    """检查文件并转换 PDF 为 Word"""
    if not os.path.exists(filepath):
        return f"文件路径不存在：{filepath}"
    if filepath.lower().endswith('.pdf'):
        # 生成转换后的 Word 文件路径
        word_filepath = os.path.splitext(filepath)[0] + '.docx'
        try:
            convert_pdf_to_docx(filepath, word_filepath)
            return f"文件已成功转换为 Word 格式：{word_filepath}"
        except Exception as e:
            return f"文件转换失败: {filepath}, 错误: {str(e)}"
    elif filepath.lower().endswith('.docx'):
        # 生成转换后的 Word 文件路径
        word_filepath = os.path.splitext(filepath)[0] + '.pdf'
        try:
            convert_pdf_to_docx(filepath, word_filepath)
            return f"文件已成功转换为PDF格式：{word_filepath}"
        except Exception as e:
            return f"文件转换失败: {filepath}, 错误: {str(e)}"
    else:
        return "文件不是 PDF 格式，无法转换。"


def convert_pdf_to_docx(pdf_path, docx_path):
    """ 将单个PDF文件转换为Word格式 """
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()


def convert_docx_to_pdf(docx_path, pdf_path):
    try:
        # 调用 docx2pdf.convert 方法进行转换
        convert(docx_path, pdf_path)
        # 检查文件是否成功生成
        if os.path.exists(pdf_path):
            print(f"文件已成功转换为 PDF: {pdf_path}")
        else:
            print(f"转换后未生成 PDF: {pdf_path}")
    except Exception as e:
        print(f"文件转换失败，错误: {str(e)}")



def convert_excel_to_csv(excel_path, csv_path):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_path)

        # 将数据框写入 CSV 文件
        df.to_csv(csv_path, index=False)  # 不保留行索引
        print(f"成功将 {excel_path} 转换为 {csv_path}")
    except Exception as e:
        print(f"转换失败：{e}")
