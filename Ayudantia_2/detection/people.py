from ultralytics import YOLO
import cv2

model = YOLO("yolo26m.pt")
results = model("./data/image.jpg")

for r in results:
    img = r.orig_img.copy()

    for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
        x1, y1, x2, y2 = map(int, box)

        label = r.names[int(cls)]
        text = f"{label} {conf:.2f}"

        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(img, text, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv2.imshow("YOLO", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
