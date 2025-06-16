from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Use lightweight summarizer model
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

led_model = AutoModelForSeq2SeqLM.from_pretrained("allenai/led-base-16384")
led_tokenizer = AutoTokenizer.from_pretrained("allenai/led-base-16384")


def summarize_text(text: str, threshold: int = 1024):
    try:
        if len(text.split()) <= threshold:
            # Use BART for short text
            summary = bart_summarizer(text, max_length=200, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        else:
            # Use LED for long text
            inputs = led_tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=16384)
            input_ids = inputs.input_ids
            attention_mask = inputs.attention_mask

            # Set global attention on first token
            global_attention_mask = torch.zeros_like(attention_mask)
            global_attention_mask[:, 0] = 1

            summary_ids = led_model.generate(input_ids, attention_mask=attention_mask,
                                             global_attention_mask=global_attention_mask,
                                             max_length=512, num_beams=4, early_stopping=True)
            return led_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    except Exception as e:
        return f"Summarization failed: {str(e)}"