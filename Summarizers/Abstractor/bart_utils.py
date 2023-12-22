from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig

def run_bart_beam(asin_text, numBeam):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer.batch_encode_plus([asin_text],return_tensors = 'pt', max_length = 1024)
    summary_ids = model.generate(inputs["input_ids"], num_beams=numBeam, max_length=400, min_length = 320)
    bart_summary = tokenizer.decode(summary_ids[0],skip_special_tokens = True)


    return bart_summary