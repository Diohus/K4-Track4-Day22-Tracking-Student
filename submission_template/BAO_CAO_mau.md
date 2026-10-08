# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** [điền số nhóm]

**Thành viên:** [điền tên hai thành viên]

Detector cố định: `yolo26n.pt`, ảnh 640 px, lớp người; Re-ID cố định: `osnet_x0_25_msmt17.pt`. Mỗi video đã được thử trên 150 frame với ByteTrack và BoT-SORT. Sau đó thử riêng `conf` 0.15 / 0.3 / 0.5 và `iou` 0.4 / 0.5 / 0.7 trên tracker được cân nhắc. Các file trong `runs/nop_bai/` dùng toàn bộ frame.

## 1. Giả thuyết trước khi thử

- `video_2`: Cảnh đông và tối dễ làm hộp người chồng nhau. Re-ID có thể giúp nhận lại người sau che khuất, nhưng ảnh người quá nhỏ cũng có thể tạo nhiều track ngắn.
- `video_3`: Camera di chuyển và ít frame mỗi giây khiến vị trí người đổi mạnh giữa hai frame. BoT-SORT có thể giữ thêm người nhỏ so với ByteTrack.
- `video_4`: Kính và mặt sàn phản chiếu có thể tạo hộp giả; cần kiểm tra xem hạ `conf` có giúp tìm người xa mà không tăng nhiều hộp trên phản chiếu hay không.

## 2. Cấu hình đã chọn

| Video | Tracker | conf | iou | Quan sát trên khung hình có vẽ ID | Đã thử nhưng loại |
|---|---|---:|---:|---|---|
| video_1 | botsort | 0.30 | 0.70 | Người đi gần camera có ID rõ; nhiều người xa vẫn bị bỏ sót. Cấu hình này có HOTA cao nhất trong các lượt đã chấm. | ByteTrack 0.30/0.50: HOTA 26.912, IDF1 25.713, thấp hơn. BoT-SORT 0.15/0.70 có thêm hộp nhưng HOTA giảm còn 29.664 và FP tăng. |
| video_2 | bytetrack | 0.30 | 0.50 | Người đi gần camera có hộp khá ổn; nhiều người nhỏ, sát nhau ở phía xa vẫn thiếu ID. Trong 150 frame đầu, ByteTrack tạo 16 ID và BoT-SORT tạo 23 ID. | BoT-SORT 0.30/0.50: thêm hộp ở vùng đông nhưng nhiều ID ngắn hơn. `conf=0.50` giảm số hàng kết quả từ 1.313 xuống 1.122 trong 150 frame. |
| video_3 | botsort | 0.15 | 0.50 | Một số người rất nhỏ phía xa và người sát mép ảnh có thêm hộp khi hạ `conf`; hộp ở tiền cảnh vẫn hiện diện. | ByteTrack 0.30/0.50 bỏ sót nhiều người hơn trong 150 frame đầu (593 so với 765 hàng ở BoT-SORT 0.30/0.50). `conf=0.50` chỉ còn 569 hàng. |
| video_4 | botsort | 0.30 | 0.50 | Người đi trong hành lang, kể cả người xa sau nhóm tiền cảnh, có ID; kính phản chiếu vẫn là nguồn nhầm lẫn. | `conf=0.50` giảm số hàng từ 958 xuống 782 trong 150 frame. `conf=0.15` thêm ít người xa nhưng có nguy cơ nhận phản chiếu, nên giữ 0.30. |
| video_5 | botsort | 0.30 | 0.50 | Khi camera tiến qua giao lộ, BoT-SORT đánh dấu thêm nhóm người bên vỉa hè trái ở khung hình thử; người rất xa vẫn dễ bị bỏ sót. | ByteTrack 0.30/0.50 có 673 hàng trong 150 frame, BoT-SORT có 907 hàng; ở khung hình khoảng 100, ByteTrack bỏ sót vài người gần vỉa hè trái. `conf=0.50` làm ít hộp hơn. |

Số hàng kết quả ở bốn video không nhãn chỉ mô tả lượng hộp/track được xuất, **không phải điểm chất lượng**. `iou` là ngưỡng NMS của detector. Trong lượt thử, đổi `iou` từ 0.4 sang 0.7 ít tác động ở `video_2` và `video_4`; riêng `video_1`, 0.7 cho HOTA tốt hơn 0.5.

## 3. Số liệu video_1

Chấm `runs/nop_bai/video_1.txt` bằng `scripts/evaluate_practice.py` và TrackEval; 600/600 frame, BoT-SORT, `conf=0.30`, `iou=0.70`:

| HOTA | MOTA | IDF1 | DetA | AssA | IDSW |
|---:|---:|---:|---:|---:|---:|
| 29.969 | 19.025 | 29.703 | 18.408 | 49.061 | 33 |

Các lượt so sánh đủ frame trên `video_1`:

| Tracker | conf | iou | HOTA | MOTA | IDF1 |
|---|---:|---:|---:|---:|---:|
| bytetrack | 0.30 | 0.50 | 26.912 | 17.292 | 25.713 |
| botsort | 0.30 | 0.50 | 29.460 | 19.811 | 29.354 |
| botsort | 0.15 | 0.50 | 29.343 | 20.731 | 29.561 |
| botsort | 0.30 | 0.70 | **29.969** | 19.025 | 29.703 |
| botsort | 0.15 | 0.70 | 29.664 | 20.327 | **29.878** |

`video_2` đến `video_5` không có nhãn trong gói lab; không có HOTA, MOTA hoặc IDF1 cho các video này.

## 4. Phân tích

**Video_1.** BoT-SORT cho HOTA và IDF1 cao hơn ByteTrack ở cùng `conf=0.30`, `iou=0.50`, vì vậy nhóm chọn BoT-SORT để thử ngưỡng tiếp. Nâng `iou` lên 0.70 tăng HOTA từ 29.460 lên 29.969; IDF1 cũng tăng từ 29.354 lên 29.703. Đánh đổi là FP tăng từ 337 lên 611 và IDSW từ 25 lên 33, khiến MOTA giảm từ 19.811 xuống 19.025. Nhóm ưu tiên HOTA như thước đo tổng cho video có nhãn.

**Video_2.** Camera đứng yên nên dự đoán chuyển động giữa các frame dễ hơn, dù cảnh tối và đông vẫn làm nhiều người phía xa bị bỏ sót. Trên đoạn thử, BoT-SORT xuất nhiều hộp hơn nhưng cũng tạo nhiều ID mới hơn (23 so với 16), nên nhóm chọn ByteTrack để hạn chế track rời rạc. Đây là quyết định theo quan sát, không phải kết luận từ điểm số vì video này không có nhãn.

**Video_3.** Camera di chuyển và ảnh nhỏ khiến người phía xa chỉ chiếm ít pixel. BoT-SORT đánh dấu thêm người so với ByteTrack trong đoạn thử, đặc biệt khi giảm `conf` từ 0.30 xuống 0.15. Ngưỡng thấp hơn cũng có thể thêm hộp giả; nhóm ưu tiên giảm bỏ sót người nhỏ và sẽ xem kỹ các đoạn camera đổi hướng nếu có thêm thời gian.

**Video_4 và video_5.** Ở hành lang, BoT-SORT giữ hộp cho người xa sau nhóm tiền cảnh; ảnh phản chiếu là nguồn nhầm lẫn nên nhóm không giảm `conf` xuống 0.15. Ở góc nhìn trên xe, BoT-SORT thấy thêm người sát vỉa hè khi ByteTrack bỏ qua; chuyển động camera làm việc nối ID khó hơn. Hai lựa chọn này dựa trên video thử và số hàng kết quả để đối chiếu, không được diễn giải thành độ chính xác định lượng.

## 5. Nếu có thêm thời gian

Xem liên tục các đoạn người cắt nhau và các đoạn camera rung mạnh, ghi cụ thể frame đổi ID hoặc hộp giả. Sau đó thử ngưỡng `conf` mịn hơn quanh cấu hình đã chọn trên các đoạn đó.
