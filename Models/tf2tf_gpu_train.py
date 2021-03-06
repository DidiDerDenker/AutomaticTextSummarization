# Imports
import datasets
import transformers
import tf2tf_gpu_config as config
import tf2tf_gpu_helpers as helpers


# Main
tokenizer, tf2tf = helpers.load_tokenizer_and_model(from_checkpoint=False)
train_data, val_data, test_data = helpers.load_data()
rouge = datasets.load_metric("rouge")

helpers.test_cuda()
helpers.explore_corpus(train_data)
helpers.empty_cache()

tf2tf = helpers.configure_model(tf2tf, tokenizer)
tf2tf.to("cuda")


def process_data_to_model_inputs(batch):
    encoder_max_length = 512
    decoder_max_length = 128

    inputs = tokenizer(batch["text"], padding="max_length",
                       truncation=True, max_length=encoder_max_length)

    outputs = tokenizer(batch["summary"], padding="max_length",
                        truncation=True, max_length=decoder_max_length)

    batch["input_ids"] = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask
    batch["decoder_input_ids"] = outputs.input_ids
    batch["decoder_attention_mask"] = outputs.attention_mask
    batch["labels"] = outputs.input_ids.copy()
    batch["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels]
                       for labels in batch["labels"]]

    return batch


train_data = train_data.map(
    process_data_to_model_inputs,
    batched=True,
    batch_size=config.batch_size,
    remove_columns=["text", "summary"]
)

train_data.set_format(
    type="torch",
    columns=["input_ids",
             "attention_mask",
             "decoder_input_ids",
             "decoder_attention_mask",
             "labels"]
)

val_data = val_data.map(
    process_data_to_model_inputs,
    batched=True,
    batch_size=config.batch_size,
    remove_columns=["text", "summary"]
)

val_data.set_format(
    type="torch",
    columns=["input_ids",
             "attention_mask",
             "decoder_input_ids",
             "decoder_attention_mask",
             "labels"]
)


def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    rouge_output = rouge.compute(
        predictions=pred_str,
        references=label_str,
        rouge_types=["rouge2"]
    )["rouge2"].mid

    return {
        "rouge2_precision": round(rouge_output.precision, 4),
        "rouge2_recall": round(rouge_output.recall, 4),
        "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
    }


if "mbart" in config.model_name:
    training_args = transformers.TrainingArguments(
        output_dir=config.path_output,
        logging_dir=config.path_output,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=1,
        warmup_steps=500,
        weight_decay=0.01
    )

    trainer = transformers.Trainer(
        model=tf2tf,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=val_data
    )

else:
    training_args = transformers.Seq2SeqTrainingArguments(
        predict_with_generate=True,
        evaluation_strategy="steps",
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        output_dir=config.path_output,
        warmup_steps=1000,
        save_steps=10000,
        logging_steps=2000,
        eval_steps=10000,
        save_total_limit=1,
        learning_rate=5e-5,
        adafactor=True,
        fp16=True
    )

    trainer = transformers.Seq2SeqTrainer(
        model=tf2tf,
        args=training_args,
        compute_metrics=compute_metrics,
        train_dataset=train_data,
        eval_dataset=val_data,
        tokenizer=tokenizer
    )

trainer.train()
