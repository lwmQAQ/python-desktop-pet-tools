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
            convert_docx_to_pdf(filepath, word_filepath)
            return f"文件已成功转换为PDF格式：{word_filepath}"
        except Exception as e:
            return f"文件转换失败: {filepath}, 错误: {str(e)}"
    elif filepath.lower().endswith('.xls') or filepath.lower().endswith('.xlsx'):
        # 生成转换后的 Word 文件路径
        word_filepath = os.path.splitext(filepath)[0] + '.csv'
        try:
            convert_excel_to_csv(filepath, word_filepath)
            return f"文件已成功转换为CSV格式：{word_filepath}"
        except Exception as e:
            return f"文件转换失败: {filepath}, 错误: {str(e)}"
    elif filepath.lower().endswith('.csv'):
        # 生成转换后的 Word 文件路径
        word_filepath = os.path.splitext(filepath)[0] + '.xlsx'
        try:
            convert_csv_to_excel(filepath, word_filepath)
            return f"文件已成功转换为CSV格式：{word_filepath}"
        except Exception as e:
            return f"文件转换失败: {filepath}, 错误: {str(e)}"
    else:
        return "文件格式不支持"


def convert_pdf_to_docx(pdf_path, docx_path):
    """ 将单个PDF文件转换为Word格式 """
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()


def convert_docx_to_pdf(docx_path, pdf_path):
    # 调用 docx2pdf.convert 方法进行转换
    return convert(docx_path, pdf_path)


def convert_excel_to_csv(excel_path, csv_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_path)

    # 将数据框写入 CSV 文件
    return df.to_csv(csv_path, index=False)  # 不保留行索引


def convert_csv_to_excel(csv_path, excel_path):
    # 读取 CSV 文件
    df = pd.read_csv(csv_path)
    # 将数据保存为 Excel 文件
    return df.to_excel(excel_path, index=False, engine='openpyxl')  # 使用 openpyxl 写入 Excel
