# HVA Fine-Tuning Lab Notes

## Theory: Parameter-Efficient Fine-Tuning (PEFT)
Fine-tuning a large language model (LLM) usually involves updating all its parameters, which is computationally expensive. **PEFT** methods, such as **LoRA (Low-Rank Adaptation)**, freeze the pre-trained model weights and inject trainable rank decomposition matrices into each layer of the Transformer architecture. This greatly reduces the number of trainable parameters for downstream tasks.

## QLoRA
**QLoRA (Quantized LoRA)** takes this a step further by backpropagating gradients through a frozen, 4-bit quantized pretrained language model into Low Rank Adapters. This allows fine-tuning 65B parameter models on a single 48GB GPU while preserving full 16-bit fine-tuning task performance.

In HVA, we use QLoRA to adapt **Qwen 2.5 (3B)** to our specific routing tasks.

## The HVA Experiment
We are fine-tuning Qwen to improve its ability to:
1.  **Route Intents**: Accurately distinguishing between `voice_command`, `session_note`, and `conversation`.
2.  **Extract Data**: structured extraction of events and tasks from Arabic voice input.

### Dataset Structure
Our dataset `dataset_hva_qwen_routing.jsonl` follows the Alpaca format:
- **Instruction**: The system prompt or task description.
- **Input**: The user's raw voice transcript (Arabic).
- **Output**: The desired JSON structure or action.
