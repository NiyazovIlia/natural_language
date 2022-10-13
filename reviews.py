import random

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os


class BertClassifier:

    def __init__(self, model_path, tokenizer_path, n_classes=2, epochs=1, model_save_path='/content/bert.bin'):
        self.model = torch.load(model_path, map_location=torch.device('cpu'))
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model_save_path = model_save_path
        self.max_len = 512
        self.epochs = epochs
        self.out_features = self.model.bert.encoder.layer[1].output.dense.out_features
        self.model.classifier = torch.nn.Linear(self.out_features, n_classes)
        self.model.to(self.device)

    def predict(self, text):
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=512,
            return_token_type_ids=False,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        out = {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }

        input_ids = out["input_ids"].to(self.device)
        attention_mask = out["attention_mask"].to(self.device)

        outputs = self.model(
            input_ids=input_ids.unsqueeze(0),
            attention_mask=attention_mask.unsqueeze(0)
        )

        prediction = torch.argmax(outputs.logits, dim=1).cpu().numpy()[0]

        return prediction


def main(text):
    classifier = BertClassifier(
        model_path='bert.bin',
        tokenizer_path='cointegrated/rubert-tiny',
        n_classes=2,
        epochs=2,
        model_save_path='bert2.bin'
    )
    pred_test = classifier.predict(text)
    reviews_bad = ['Мне очень жаль, я исправлюсь', 'Я вас понял, мне есть куда расти',
                   'Плохой, плохой бот, как он так мог']
    reviews_good = ['Я очень рад что смог вам помочь', 'Это просто великолепно', 'Супер, супер я буду стараться']
    if pred_test == 0:
        text_finish_number = random.randint(0, len(reviews_bad) - 1)
        text_finish = reviews_bad[text_finish_number]
    else:
        text_finish_number = random.randint(0, len(reviews_good) - 1)
        text_finish = reviews_good[text_finish_number]

    return text_finish
