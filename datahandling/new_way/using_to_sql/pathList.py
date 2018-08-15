# -*- coding: utf-8 -*-

import os

# 디렉토리 목록 및 특정 파일의 목록을 가지고 오는 클래스
class PathList(object):
    """
    path_type 기본 디폴트는 파일 목록을 가지고 오는 것! 디렉토리의 목록을 가지고 오고 싶다면 꼭, path_type에 dir를 입력할 것.
    """
    def __init__(self, path, path_type=None):
        self.path = path
        self.path_type = path_type
        
    # Call a list of files from directory path
    def get_path_list(self, sign=None):
        path_list = []
        if self.path_type == 'dir':
            for file_path, dir, files in os.walk(self.path):
                for d in dir:
                    full_filename = os.path.join(file_path, d)
                    path_list.append(full_filename)
        elif self.path_type == 'file' or self.path_type == None:
            for file_path, dir, files in os.walk(self.path):
                for filename in files:
                    full_filename = os.path.join(file_path, filename)
                    ext = os.path.splitext(filename)[-1]
                    if sign == None:
                        path_list.append(full_filename)
                    elif sign == ext:
                        path_list.append(full_filename)
        return path_list
        


"""
dirpathlist = PathList('C:\\', 'dir').get_path_list()
filepathlist = []
for dirpath in dirpathlist:
    tmp = PathList(dirpath).get_path_list('.py')
    if not tmp:
        pass
    else:
        filepathlist.append(tmp)
"""