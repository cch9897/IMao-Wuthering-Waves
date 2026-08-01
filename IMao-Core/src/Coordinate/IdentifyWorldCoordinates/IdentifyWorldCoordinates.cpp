#include "IdentifyWorldCoordinates.h"
#include "..\..\util.h"
#include "..\locationCalculator\ScreenCoordinate.h"
using namespace std;
std::unique_ptr<PPOCR> IdentifyWorldCoordinates::p_ppocr;
bool IdentifyWorldCoordinates::isLoaded = false;

void IdentifyWorldCoordinates::Init(string det_model_dir, string rec_model_dir,string rec_char_dict_path,string cls_model_dir) {
	FLAGS_det_model_dir = det_model_dir;
	FLAGS_rec_model_dir = rec_model_dir;
	if (!rec_char_dict_path.empty()) {
		FLAGS_rec_char_dict_path = rec_char_dict_path;
	}
	FLAGS_cls_model_dir = cls_model_dir;
	p_ppocr = make_unique<PPOCR>();
	isLoaded = true;
}

// 放宽的坐标文本校验：允许 OCR 把坐标拆成多个文本块、置信度阈值降低、
// 分隔符允许 1~2 个（"x,y" 或 "x,y,z" 都接受），仅保留数字与分隔符。
bool IsValidSingleOCRForCoords(const vector<OCRPredictResult>& ocr_result, string& outWorldCoordinateText) {

	if (ocr_result.empty() || ocr_result.size() > 3) {
		return false;
	}

	string combined;
	for (const auto& r : ocr_result) {
		if (r.score <= 0.70) { // 原 0.85 过高，4K/缩放场景下小字置信度常低于此
			return false;
		}
		combined += UTF8ToGBK(r.text);
	}

	// 去掉空白字符（OCR 可能在数字间夹空格）
	string ocr_textResult;
	for (char c : combined) {
		if (c == ' ' || c == '	' || c == '\r' || c == '\n') {
			continue;
		}
		ocr_textResult += c;
	}

	if (ocr_textResult.empty()) {
		return false;
	}

	int i = 0;
	for (char& c : ocr_textResult) {
		if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) {
			return false;
		}

		if (c == '.' || c == ',' || c == ':' || c == '|') {
			c = '|';
			i++;
		}
	}

	// 原逻辑要求恰好 2 个分隔符（3 段）；放宽为 1~2 个（2~3 段），
	// 兼容 "x,y" 与 "x,y,z"（部分版本/界面坐标带高度或小数段）
	if (i < 1 || i > 2) {
		return false;
	}

	outWorldCoordinateText = ocr_textResult;
	return true;
}


vector<int> SplitStringToIntArray(const string& input) {
	std::vector<int> result;
	std::stringstream ss(input);
	std::string token;

	while (std::getline(ss, token, '|')) {
		try {
			result.push_back(std::stoi(token));
		}
		catch (const std::invalid_argument& e) {
			std::cerr << "输入的数字格式无效: " << token << std::endl;
		}
		catch (const std::out_of_range& e) {
			std::cerr << "数字超出范围: " << token << std::endl;
		}
	}
	return result;
}


bool IdentifyWorldCoordinates::IdentifyCoordinate(const Mat& imgCoordinates,Coordinate& outPlayerWorldCoordinate) {;
	vector<OCRPredictResult> ocr_result = p_ppocr->ocr(imgCoordinates, true, true, true);
	string playerWorldCoordinate;
	if (IsValidSingleOCRForCoords(ocr_result, playerWorldCoordinate)) {
		vector<int> pWorldCoordinateArr= SplitStringToIntArray(playerWorldCoordinate);
		if (pWorldCoordinateArr.size() >= 2) {
			Coordinate playerWorldCoordinate(pWorldCoordinateArr[0], pWorldCoordinateArr[1]);
			outPlayerWorldCoordinate = playerWorldCoordinate;
			return true;
		}
	}

	// 诊断输出：帮助定位 #10（Win11 双屏/4K 下坐标识别持续失败）
	if (IsDebuggerPresent()) {
		std::cout << "[IMao] OCR coords failed. blocks=" << ocr_result.size();
		for (const auto& r : ocr_result) {
			std::cout << " | '" << UTF8ToGBK(r.text) << "'(score=" << r.score << ")";
		}
		std::cout << std::endl;
	}
	return false;
}

bool IdentifyWorldCoordinates::IdentifyCoordinateFromSnapshot(const Mat& snapshot, Coordinate& outPlayerWorldCoordinate, RECT rect) {
	Mat imgCoordinates = ImageProcessing::CropToShowWorldCoordinateAreaImg(snapshot, rect);
	if (imgCoordinates.empty())
		return false;

	imgCoordinates = ImageProcessing::centerAndScaleImage(imgCoordinates, 2);
	return IdentifyCoordinate(imgCoordinates, outPlayerWorldCoordinate);
}

bool IdentifyWorldCoordinates::IdentifyCoordinateFromSnapshot(const Mat& snapshot, Coordinate& outPlayerWorldCoordinate, HWND w_hwnd) {
	Mat imgCoordinates = ImageProcessing::CropToShowWorldCoordinateAreaImg(snapshot, w_hwnd);
	if (imgCoordinates.empty())
		return false;

	imgCoordinates = ImageProcessing::centerAndScaleImage(imgCoordinates, 2);

	return IdentifyCoordinate(imgCoordinates, outPlayerWorldCoordinate);
}
