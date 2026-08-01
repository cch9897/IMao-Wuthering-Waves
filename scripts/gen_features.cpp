// 从 NEW MAP.png 生成 Map_features.yml（与 IMao FeatureLoader 兼容）
// 分块提取 SURF 特征避免全图 OOM，合并后写入 yml
// 用法: ./gen_features <Map.png> <out.yml> [block_size]
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/xfeatures2d/nonfree.hpp>
#include <opencv2/xfeatures2d.hpp>
#include <iostream>

using namespace cv;

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: gen_features <Map.png> <out.yml> [block=2048]" << std::endl;
        return 1;
    }
    int block = (argc > 3) ? atoi(argv[3]) : 2048;
    Mat img = imread(argv[1], IMREAD_GRAYSCALE);
    if (img.empty()) {
        std::cerr << "cannot read image" << std::endl;
        return 1;
    }
    std::cout << "image: " << img.cols << "x" << img.rows << " block=" << block << std::endl;

    Ptr<xfeatures2d::SURF> surf = xfeatures2d::SURF::create(60, 8, 4, true, true);
    std::vector<KeyPoint> allKeypoints;
    std::vector<Mat> descriptorParts;

    int totalBlocks = 0;
    for (int y = 0; y < img.rows; y += block) {
        for (int x = 0; x < img.cols; x += block) {
            int w = std::min(block, img.cols - x);
            int h = std::min(block, img.rows - y);
            Mat tile = img(Rect(x, y, w, h)).clone(); // 必须 clone（SURF 要求连续）

            std::vector<KeyPoint> kps;
            Mat desc;
            surf->detectAndCompute(tile, noArray(), kps, desc);
            if (desc.empty()) continue;

            for (auto& kp : kps) {
                kp.pt.x += x;
                kp.pt.y += y;
            }
            allKeypoints.insert(allKeypoints.end(), kps.begin(), kps.end());
            descriptorParts.push_back(desc);
            totalBlocks++;
        }
    }
    std::cout << "blocks processed: " << totalBlocks << std::endl;

    Mat allDescriptors;
    if (!descriptorParts.empty()) {
        vconcat(descriptorParts, allDescriptors);
    }
    std::cout << "keypoints: " << allKeypoints.size()
              << " descriptors: " << allDescriptors.rows << "x" << allDescriptors.cols << std::endl;

    FileStorage fs(argv[2], FileStorage::WRITE | FileStorage::FORMAT_XML);
    fs << "keypoints" << allKeypoints;
    fs << "descriptors" << allDescriptors;
    fs.release();
    std::cout << "written: " << argv[2] << std::endl;
    return 0;
}
