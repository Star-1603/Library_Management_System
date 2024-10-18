import cv2
from pyzbar import pyzbar

def decode_barcode(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ISBN: {barcode_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return barcode_data
    return None

def start_barcode_scanner():
    cap = cv2.VideoCapture(1)
    isbn = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        isbn = decode_barcode(frame)
        if isbn:
            cap.release()
            cv2.destroyAllWindows()
            return isbn
        frame_height, frame_width, _ = frame.shape
        box_x1 = frame_width // 4
        box_y1 = frame_height // 4
        box_x2 = frame_width - box_x1
        box_y2 = frame_height - box_y1
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 0, 0), 2)

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return isbn