
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# require PyTorch

model_name = "facebook/nllb-200-distilled-600M"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='eng_Latn', tgt_lang='tha_Thai', max_length = 400)
translated_text_to_th = translator("This is a very good model")
print(translated_text_to_th)

translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='tha_Thai', tgt_lang='eng_Latn', max_length = 400)
translated_text_to_en = translator("สวัสดีค่ะ ชื่ออะไรค่ะ")
print(translated_text_to_en)
