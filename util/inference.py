import torch
from util.utilities import get_transform

# Inference function

def predict_image(model, image, device, class_names, img_size=224):
    transform = get_transform(img_size)
    img_t = transform(image).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(img_t)
        probs_t = torch.softmax(outputs, dim=1)[0].cpu()
        _, predicted = outputs.max(1)

    return class_names[predicted.item()], float(probs_t[predicted.item()])

def predict_image_probs(model, image, device, class_names, img_size=224):
    """
    Trả về (predicted_label, probs_list)
    probs_list: list float, mỗi phần tử trong [0,1], chiều bằng len(class_names)
    """
    transform = get_transform(img_size)
    img_t = transform(image).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(img_t)
        probs = torch.softmax(outputs, dim=1)[0].cpu().numpy().tolist()
        _, predicted = outputs.max(1)

    predicted_label = class_names[predicted.item()]
    return predicted_label, probs