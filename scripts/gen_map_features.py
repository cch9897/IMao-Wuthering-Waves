#!/usr/bin/env python3
"""从 NEW MAP.png 重新生成 Map_features.yml（SURF 特征，OpenCV nonfree 版）。

作者原版特征（2026-01-10）只覆盖旧区域，新区域（黯原/下层金库/时隙废都）无特征，
导致这些区域无法做小地图定位匹配。用本脚本从完整地图重新提取即可覆盖全部区域。

用法:
    python3 gen_map_features.py <Map.png 路径> <输出 yml 路径>

依赖:
    conda-forge 的 opencv（默认开启 OPENCV_ENABLE_NONFREE，SURF 可用）:
    conda create -n wuwa -c conda-forge python=3.11 opencv

输出格式与 IMao FeatureLoader::loadFeaturesFromXML 兼容:
    FileStorage XML, keypoints + descriptors
"""
import sys
import cv2

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    map_path = sys.argv[1]
    out_path = sys.argv[2]

    img = cv2.imread(map_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"无法读取 {map_path}")
        sys.exit(1)
    print(f"地图尺寸: {img.shape}")

    # 与 Test/main.cpp 相同的 SURF 参数
    surf = cv2.xfeatures2d.SURF_create(60, 8, 4, True, True)
    print("提取特征中（大图需要几分钟）...")
    keypoints, descriptors = surf.detectAndCompute(img, None)
    print(f"特征点: {len(keypoints)}")

    fs = cv2.FileStorage(out_path, cv2.FILE_STORAGE_WRITE | cv2.FILE_STORAGE_FORMAT_XML)
    fs.write("keypoints", keypoints)
    fs.write("descriptors", descriptors)
    fs.release()
    print(f"已写入 {out_path}")

if __name__ == "__main__":
    main()
