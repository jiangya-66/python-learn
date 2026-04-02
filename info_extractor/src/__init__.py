"""
info_extractor.src - 信息抽取器源代码包
"""

# import sys
# import os.path as osp

# # 当作为脚本直接运行时，添加必要的路径
# if __name__ == "__main__" or not __package__:
#     current_dir = osp.dirname(osp.abspath(__file__))
#     project_root = osp.dirname(osp.dirname(current_dir))
#     if project_root not in sys.path:
#         sys.path.insert(0, project_root)
    
#     # 使用绝对导入
#     from .extractor import InfoExtractor, ReviewAnalysis, Sentiment
#     from .utils import validate_api_key, summarize_results, format_results_for_display
# else:

# 正常作为包的一部分导入
from .models import ReviewAnalysis, Sentiment
from .extractor import InfoExtractor
from .utils import validate_api_key, summarize_results, format_results_for_display

__all__ = [
    'ReviewAnalysis',
    'Sentiment',
    'InfoExtractor',
    'validate_api_key',
    'summarize_results',
    'format_results_for_display',
]
