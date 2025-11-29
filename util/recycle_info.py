RECYCLABLE_INFO = {
    'cardboard': ('Tái chế được', 'Bìa carton khô và sạch có thể tái chế.'),
    'paper': ('Tái chế được', 'Giấy sạch có thể tái chế; giấy dơ/ướt không nên.'),
    'plastic': ('Tái chế được', 'Nhiều loại nhựa tái chế được; nhựa dơ/thực phẩm khó tái.'),
    'glass': ('Tái chế được', 'Thủy tinh tái chế tốt.'),
    'metal': ('Tái chế được', 'Nhôm, sắt, thép tái chế tốt.'),
    'battery': ('Tái chế đặc biệt', 'Pin phải thu gom riêng và xử lý bởi cơ sở chuyên dụng.'),
    'biological': ('Không tái chế', 'Rác hữu cơ — nên ủ compost nếu có thể.'),
    'clothes': ('Không tái chế', 'Quần áo thường không tái chế trong hệ thống dân dụng; có thể tái sử dụng/hiến tặng.'),
    'shoes': ('Không tái chế', 'Giày làm từ nhiều vật liệu trộn — khó tái chế.'),
    'trash': ('Không tái chế', 'Rác hỗn hợp/bẩn — không tái chế.')
}

def get_recycle_info(label: str):
    """
    Trả về tuple (status, note) cho label. Nếu không có, trả ('Không xác định','Không có thông tin.')
    """
    return RECYCLABLE_INFO.get(label, ('Không xác định', 'Không có thông tin.'))