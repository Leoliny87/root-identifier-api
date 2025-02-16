#!/bin/bash
# 自动下载LFS文件并复制到正确位置

echo "=== 开始处理模型文件 ==="

# 初始化LFS
git lfs install

# 拉取大文件（关键步骤）
git lfs pull

# 创建目标目录
mkdir -p api/model

# 复制模型文件到API目录
cp model/*.h5 api/model/

echo "=== 模型文件处理完成 ==="
