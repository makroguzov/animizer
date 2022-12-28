import json
import pathlib
import re
import string
import typing

import nltk
import nltk.corpus as corpus
import numpy as np
import torch
import torch.nn as nn


class Model:
    _RUSSIAN_STOP_WORDS = corpus.stopwords.words('russian')
    _REMOVE_OTHERS_PATTERN = re.compile(r'[^А-яЁё]+')
    _TRANSLATE_PATTERN = re.compile(r'[Ёё]+')
    _TOKENIZER = nltk.tokenize.WordPunctTokenizer()
    _PUNCTUATION = set(string.punctuation)
    _UNK_ID = 0
    _PAD_ID = 1

    def __init__(self, path: str):
        token_path = pathlib.Path(f'{path}/token.txt').resolve()
        if token_path.exists():
            self.token_ids = json.load(token_path.open())
        else:
            raise ValueError('Ошибка!!!')

        self._model = _NeuralModel(n_tokens=len(self.token_ids),
                                   concat_number_of_features=69 * 2,
                                   hid_size=69)

        model_path = pathlib.Path(f'{path}/model').resolve()
        if model_path.exists():
            self._model.load_state_dict(torch.load(model_path))
        else:
            raise ValueError('Ошибка!!!')

    def predict(self, title: str, descr: str) -> float:
        return self._model((
            torch.tensor(self._matrix([self._normalize(title)]), dtype=torch.int64),
            torch.tensor(self._matrix([self._normalize(descr)]), dtype=torch.int64)
        ))

    def _normalize(self, text: str):
        text = text.lower()
        text = self._REMOVE_OTHERS_PATTERN.sub(' ', text).strip()
        text = self._TRANSLATE_PATTERN.sub('е', text)
        text = self._TOKENIZER.tokenize(text)
        text = [
            word for word in text
            if word not in self._RUSSIAN_STOP_WORDS and word not in self._PUNCTUATION
        ]
        return ' '.join(text)

    def _matrix(self, seq: typing.Sequence[str], max_len=None):
        seq = [s.split() for s in seq]
        max_len = min(max(map(len, seq)), max_len or float('inf'))

        matrix_shape = len(seq), max_len
        matrix = np.full(matrix_shape, np.int32(self._PAD_ID))

        for i, tokens in enumerate(seq):
            row = [self.token_ids.get(word, self._UNK_ID) for word in tokens[:max_len]]
            matrix[i, :len(row)] = row

        return matrix


class _MaxPooling(nn.Module):

    def __init__(self, dim=-1):
        super().__init__()
        self.dim = dim

    def forward(self, x):
        return x.max(dim=self.dim)[0]


class _NeuralModel(nn.Module):

    def __init__(self,
                 n_tokens: int,
                 concat_number_of_features: int,
                 hid_size: int = 69) -> None:
        super().__init__()
        self.t_embedding = nn.Embedding(num_embeddings=n_tokens,
                                        embedding_dim=hid_size)
        self.f_embedding = nn.Embedding(num_embeddings=n_tokens,
                                        embedding_dim=hid_size)

        self.conv1 = nn.Conv1d(hid_size, hid_size, kernel_size=3, padding=1)
        self.dense = nn.Linear(hid_size, hid_size)
        self.pool = _MaxPooling()

        self.inter_dense = nn.Linear(in_features=concat_number_of_features,
                                     out_features=2 * hid_size)
        self.final_dense = nn.Linear(in_features=2 * hid_size, out_features=1)

    def forward(self, input_data: tuple):
        i1, i2 = input_data

        title = self.t_embedding(i1).permute((0, 2, 1))
        title = self.conv1(title)
        title = self.pool(title)
        title = nn.ReLU()(title)
        title = self.dense(title)

        fulld = self.f_embedding(i2).permute((0, 2, 1))
        fulld = self.conv1(fulld)
        fulld = self.pool(fulld)
        fulld = nn.ReLU()(fulld)
        fulld = self.dense(fulld)

        concat_arrays = [
            title.view(title.size(0), -1),
            fulld.view(fulld.size(0), -1),
        ]

        out = nn.Sequential(self.inter_dense, nn.ReLU(), self.final_dense)

        return out(torch.cat(concat_arrays, dim=1))
