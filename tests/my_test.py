from transformers import AutoModelForCausalLM
from peft import PeftModel

def count_trainable_parameters(model):
    count = 0
    for param in model.parameters():
        if param.requires_grad:
            count += 1
            
    return count

def get_nb_trainable_parameters(self) -> tuple[int, int]:
    r"""
    Returns the number of trainable parameters and the number of all parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in self.named_parameters():
        num_params = param.numel()
        # if using DS Zero 3 and the weights are initialized empty
        if num_params == 0 and hasattr(param, "ds_numel"):
            num_params = param.ds_numel

        # Due to the design of 4bit linear layers from bitsandbytes
        # one needs to multiply the number of parameters by 2 to get
        # the correct number of parameters
        if param.__class__.__name__ == "Params4bit":
            if hasattr(param, "element_size"):
                num_bytes = param.element_size()
            elif not hasattr(param, "quant_storage"):
                num_bytes = 1
            else:
                num_bytes = param.quant_storage.itemsize
            num_params = num_params * 2 * num_bytes

        all_param += num_params
        if param.requires_grad:
            trainable_params += num_params

    return trainable_params, all_param

model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/ChipSeek-R1/output/Qwen3-1.7B/merge_lora")
print(get_nb_trainable_parameters(model))
model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/ChipLLM/llm-models/Qwen3-1.7B")
print(get_nb_trainable_parameters(model))
lora_model = PeftModel.from_pretrained(model, "/root/autodl-tmp/ChipSeek-R1/output/Qwen3-1.7B/sft/lora", is_trainable = True)
# lora_model.print_trainable_parameters()
print(get_nb_trainable_parameters(lora_model))

# ----------------------------------------------------------------------

# from transformers import AutoModelForCausalLM

# def check_requires_grad(model):
#     for name, param in model.named_parameters():
#         print(f"{name}: requires_grad = {param.requires_grad}")

# 加载 merge_lora 模型
# model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/ChipSeek-R1/output/Qwen3-1.7B/merge_lora")
# check_requires_grad(lora_model)
