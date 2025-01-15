import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model
model_path = "./deployed_model"
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Dummy input for tracing (including both input_ids and decoder_input_ids)
dummy_input = {
    "input_ids": torch.randint(0, 32128, (1, 512)),  # Adjust for your tokenizer vocab size
    "attention_mask": torch.ones((1, 512)),  # Attention mask
    "decoder_input_ids": torch.randint(0, 32128, (1, 150)),  # Dummy decoder input ids
}

# Export the model to ONNX with opset_version=14
onnx_model_path = "./deployed_model/t5_model.onnx"
torch.onnx.export(
    model,
    (dummy_input["input_ids"], dummy_input["attention_mask"], dummy_input["decoder_input_ids"]),
    onnx_model_path,
    input_names=["input_ids", "attention_mask", "decoder_input_ids"],  # Specify decoder_input_ids here
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "decoder_input_ids": {0: "batch_size", 1: "sequence_length"},
        "logits": {0: "batch_size", 1: "sequence_length"},
    },
    opset_version=14,  # Use opset version 14 or higher
)

print(f"ONNX model exported to {onnx_model_path}")
