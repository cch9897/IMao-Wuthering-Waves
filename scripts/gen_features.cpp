// 从 NEW MAP.png 生成 Map_features.yml（与 IMao FeatureLoader 兼容）
// 编译: g++ -O2 gen_features.cpp -o gen_features \
//       -I/tmp/opencv/include -I/tmp/opencv/modules/core/include -I/tmp/opencv/modules/imgproc/include \
//       -I/tmp/opencv/modules/features2d/include -I/tmp/opencv/modules/calib3d/include -I/tmp/opencv_contrib/modules/xfeatures2d/include \
//       -L/tmp/opencv/build/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_features2d -lopencv_xfeatures2d -lopencv_flann -lopencv_calib3d \
//       -Wl,-rpath,/tmp/opencv/build/lib
// 用法: ./gen_features <Map.png> <out.yml>
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
        std::cerr << "usage: gen_features <Map.png> <out.yml>" << std::endl;
        return 1;
    }
    Mat img = imread(argv[1], IMREAD_GRAYSCALE);
    if (img.empty()) {
        std::cerr << "cannot read image" << std::endl;
        return 1;
    }
    std::cout << "image: " << img.cols << "x" << img.rows << std::endl;

    // 与 Test/main.cpp 相同的 SURF 参数
    Ptr<xfeatures2d::SURF> surf = xfeatures2d::SURF::create(60, 8, 4, true, true);
    std::vector<KeyPoint> keypoints;
    Mat descriptors;
    surf->detectAndCompute(img, noArray(), keypoints, descriptors);
    std::cout << "keypoints: " << keypoints.size() << " descriptors: " << descriptors.rows << "x" << descriptors.cols << std::endl;

    FileStorage fs(argv[2], FileStorage::WRITE | FileStorage::FORMAT_XML);
    fs << "keypoints" << keypoints;
    fs << "descriptors" << descriptors;
    fs.release();
    std::cout << "written: " << argv[2] << std::endl;
    return 0;
}
