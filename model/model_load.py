import torch
import torch.nn as nn
import torchvision.models as models

def load_checkpoint(path, device, num_classes):
    checkpoint = torch.load(path, map_location=device)

    if isinstance(checkpoint, nn.Module):
        model = checkpoint
        model.to(device)
        model.eval()
        return model

    state = checkpoint.get('state_dict', checkpoint)

    # Detect output classes
    final_key = None
    for k in state.keys():
        if k.endswith('fc.weight') or k.endswith('classifier.weight'):
            final_key = k
            break

    if final_key:
        num_classes = state[final_key].shape[0]

    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Try to load
    try:
        model.load_state_dict(state)
    except Exception:
        new_state = {k.replace('module.', ''): v for k, v in state.items()}
        model.load_state_dict(new_state, strict=False)

    model.to(device)
    model.eval()
    return model
