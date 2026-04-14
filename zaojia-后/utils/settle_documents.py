import os

def read_txt(file_path: str, encoding: str = "utf-8") -> str:
    """
    读取 txt 文件并返回所有文字内容
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件未找到: {file_path}")
    
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        # 如果 utf-8 失败，尝试 gbk
        if encoding.lower() == "utf-8":
            try:
                with open(file_path, "r", encoding="gbk") as f:
                    return f.read()
            except Exception as e2:
                raise Exception(f"读取 txt 文件失败: {str(e2)}")
        raise Exception(f"读取 txt 文件失败: {str(e)}")

def read_word(file_path: str) -> str:
    """
    读取 Word 文件（兼容 .docx 和 .doc 格式）并返回所有文字内容
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件未找到: {file_path}")
    
    # 获取文件后缀
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # 处理 .docx 格式
    if file_ext == ".docx":
        try:
            import docx
        except ImportError:
            raise ImportError("未安装 python-docx 库，请使用 pip install python-docx 进行安装")
        
        try:
            document = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"读取 .docx 文件失败: {str(e)}")
    
    # 处理 .doc 格式（仅 Windows 系统）
    elif file_ext == ".doc":
        try:
            import win32com.client
        except ImportError:
            raise ImportError("未安装 pywin32 库，请使用 pip install pywin32 进行安装（仅Windows支持）")
        
        try:
            # 启动 Word 应用程序（后台运行，不显示界面）
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            
            # 打开文档并读取内容
            doc = word.Documents.Open(os.path.abspath(file_path))
            text = doc.Content.Text
            doc.Close()
            word.Quit()
            
            return text
        except Exception as e:
            raise Exception(f"读取 .doc 文件失败: {str(e)}")
    
    # 不支持的格式
    else:
        raise ValueError(f"不支持的文件格式: {file_ext}，仅支持 .docx 和 .doc")

def read_pdf(file_path: str) -> str:
    """
    读取 PDF 文件并返回所有文字内容
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件未找到: {file_path}")
        
    try:
        import PyPDF2
    except ImportError:
        raise ImportError("未安装 PyPDF2 库，请使用 pip install PyPDF2 进行安装")
        
    try:
        text = ""
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        raise Exception(f"读取 PDF 文件失败: {str(e)}")
