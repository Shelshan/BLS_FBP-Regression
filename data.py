# import os
# from PIL import Image
# image_folder = r"./datasets/MEBeauty"
# filePath_train = r'./datasets/MEBeauty/train.txt'

# import os
# import shutil

# import os

# # 定义函数，将图像重新命名并覆盖原始图像，同时更新标签并保存到新txt文件中
# def rename_and_save(txt_file_path, new_txt_file_path):
#     # 读取txt文件中的内容到list中
#     with open(txt_file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
    
#     # 创建新的txt文件
#     new_f = open(new_txt_file_path, 'w', encoding='utf-8')

#     # 计数器，从1开始给图像进行新命名
#     count = 1

#     # 遍历txt中的每一行
#     for line in lines:
#         image_path, label = line.strip().split()
#         image_path = os.path.join(image_folder, image_path)

#         # 处理图像
#         if os.path.isfile(image_path):
#             # 构造新的图像名称
#             image_ext = os.path.splitext(image_path)[1]
#             new_image_name = 'new_image_{}.{}'.format(count, image_ext)

#             # 构造新的图像路径
#             new_image_path = os.path.join(os.path.dirname(image_path), new_image_name)

#             # 重命名图像文件
#             os.rename(image_path, new_image_path)

#             # 将新的图像名称和对应的标签写入新的txt文件中
#             new_f.write('{} {}\n'.format(new_image_path, label))

#             # 计数器加1
#             count += 1
#         else:
#             print('图片不存在：{}'.format(image_path))

#     # 关闭文件
#     new_f.close()

# # 测试
# txt_file_path = r'./datasets/MEBeauty/train.txt'
# new_txt_file_path = 'new_image_labels.txt'

# rename_and_save(txt_file_path, new_txt_file_path)

import openpyxl

# 定义函数，读取xlsx文件的第一列和第二列，并保存到txt文件中
# def save_columns_to_txt(xlsx_file_path, txt_file_path):
#     # 打开xlsx文件
#     wb = openpyxl.load_workbook(xlsx_file_path)

#     # 获取当前活动的工作表
#     ws = wb.active

#     # 打开txt文件
#     f = open(txt_file_path, 'w')

#     # 遍历每一行，将第一列和第二列的内容写入txt文件中
#     for row in ws.iter_rows(values_only=True):
#         if row[0] is not None and row[1] is not None:
#             line = '{}.jpg {}\n'.format(row[0], row[1])
#             f.write(line)

#     # 关闭文件
#     f.close()

# # 测试
# xlsx_file_path = 'Attractiveness label.xlsx'
# txt_file_path = 'data.txt'

# save_columns_to_txt(xlsx_file_path, txt_file_path)

# def process_txt_file(txt_file_path):
#     # 打开txt文件
#     with open(txt_file_path, 'r') as f:
#         # 逐行读取文件内容
#         lines = f.readlines()

#     # 处理每一行的内容
#     processed_lines = []
#     for line in lines:
#         # 分割每一行的数据
#         columns = line.strip().split(' ')
#         if len(columns) >= 2:
#             # 在图像名称前面添加"SCUT-FBP-"
#             new_line = 'SCUT-FBP-' + columns[0] + ' ' + ' '.join(columns[1:]) + '\n'
#             processed_lines.append(new_line)

#     # 将处理后的结果写入新的txt文件
#     processed_txt_file_path = 'processed_data.txt'
#     with open(processed_txt_file_path, 'w') as f:
#         f.writelines(processed_lines)

# # 测试
# txt_file_path = 'data.txt'
# process_txt_file(txt_file_path)

import random

def split_txt_file(txt_file_path, train_ratio=0.6):
    # 打开txt文件
    with open(txt_file_path, 'r') as f:
        # 逐行读取文件内容
        lines = f.readlines()

    # 将数据随机打乱
    random.shuffle(lines)

    # 计算训练集和测试集的大小
    num_lines = len(lines)
    num_train_lines = int(num_lines * train_ratio)
    num_test_lines = num_lines - num_train_lines

    # 拆分训练集和测试集
    train_lines = lines[:num_train_lines]
    test_lines = lines[num_train_lines:]

    # 将训练集和测试集写入新的txt文件
    train_txt_file_path = 'train.txt'
    with open(train_txt_file_path, 'w') as f:
        f.writelines(train_lines)

    test_txt_file_path = 'test.txt'
    with open(test_txt_file_path, 'w') as f:
        f.writelines(test_lines)

# 测试
txt_file_path = 'processed_data.txt'
split_txt_file(txt_file_path, train_ratio=0.6)

# # 读取txt文件中的内容
# with open(r'./datasets/MEBeauty/test.txt', 'r', encoding='utf-8') as file:
#     lines = file.read().splitlines()

# image_paths = []
# labels = []

# # 遍历每一行
# for line in lines:
#     parts = line.split()  # 使用空格分隔每一行的内容
#     image_path = os.path.join(image_folder, parts[0])  # 第一个部分为图像路径
#     label = ' '.join(parts[1:])  # 剩余部分为标签，使用空格连接起来

#     if os.path.exists(image_path):
#         # 图片存在，则进行读取和处理
#         # image_path = os.path.join(image_folder, image_path)
#         image = Image.open(image_path)
#         # 进行图片处理操作
#         # ...

#         # 示例：展示图片
#         # image.show()

#         # 将存在的图像路径和标签添加到列表中
#         image_paths.append(image_path)
#         labels.append(label)
#     else:
#         # 图片不存在，打印提示信息，并从列表中删除该路径和标签
#         print(f"图片不存在：{image_path}")

# # 删除不存在的图片路径和标签后，将剩余的路径和标签重新写入txt文件
# with open('test.txt', 'w', encoding='utf-8') as file:
#     for i in range(len(image_paths)):
#         file.write(f"{image_paths[i]} {labels[i]}\n")