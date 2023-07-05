# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the GNU General Public License version 3.

import os
from logging import getLogger
from typing import List

from sentencepiece import SentencePieceProcessor

logger = getLogger()

current_file_path = os.path.abspath(__file__)
model_path = os.path.join(os.path.dirname(current_file_path), 'tokenizer.model')

class LLaMATokenizer:
    def __init__(self, model_path = model_path):
        # reload tokenizer
        assert os.path.isfile(model_path), model_path
        self.sp_model = SentencePieceProcessor(model_file=model_path)
        logger.info(f"Reloaded SentencePiece model from {model_path}")

        # BOS / EOS token IDs
        self.n_words: int = self.sp_model.vocab_size()
        self.bos_id: int = self.sp_model.bos_id()
        self.eos_id: int = self.sp_model.eos_id()
        self.pad_id: int = self.sp_model.pad_id()
        logger.info(
            f"#words: {self.n_words} - BOS ID: {self.bos_id} - EOS ID: {self.eos_id}"
        )
        assert self.sp_model.vocab_size() == self.sp_model.get_piece_size()

    def encode(self, s: str, bos: bool, eos: bool) -> List[int]:
        assert type(s) is str
        t = self.sp_model.encode(s)
        if bos:
            t = [self.bos_id] + t
        if eos:
            t = t + [self.eos_id]
        return t

    def decode(self, t: List[int]) -> str:
        return self.sp_model.decode(t)


tokenizer = LLaMATokenizer()

# 某些 token 单独拿去 decode，会返回预期之外的值，在此特判
# 注意，key 为字符串
SPECIAL_TOKEN_DICT ={
    # 空格
    '29871' : ' ',
    # 仅做演示，此处使用 + 连接两个 token
    '12345+54321' : '<UNKNOWN>'
}

def conv(tokens, text):
    print(f'text [{text}]')
    segments = []
    token_acc = []
    for idx in range(len(tokens)):
        # 根据 decode 得到的字符，跟 chars 中的比较
        token_acc.append({'id':tokens[idx], 'idx':idx})

        decoded = tokenizer.decode([x['id'] for x in token_acc])
        decode_len = len(decoded)

        # 可能出现特殊情况，需要特判
        if decode_len == 0:
            check_key = "+".join([str(x['id']) for x in token_acc])
            if check_key in SPECIAL_TOKEN_DICT:
                decoded = SPECIAL_TOKEN_DICT[check_key]
                decode_len = len(decoded)
            else:
                print(check_key)
                continue
        print(f'*[{decoded}]', text[:decode_len])
        # 某些 emoji 或者汉字会使用多个 token 来表示
        # 解析结果与原始字符串相同时，塞入一个结果，否则继续 append 导 token_acc
        txt_to_check = text[:decode_len]
        print(f'to check[{txt_to_check}]')
        if decoded == txt_to_check:
            segments.append({
                'text': txt_to_check,
                'tokens': token_acc.copy()
            })
            text = text[decode_len:]
            print(text, decode_len)
            print(segments)
            token_acc = []

    return segments

def encode(text):
    ids = tokenizer.encode(text, False, False)
    print(ids)
    
    if len(ids) and str(ids[0]) in SPECIAL_TOKEN_DICT:
        text = SPECIAL_TOKEN_DICT[str(ids[0])] + text
    return conv(ids, text)
    
print('[{tokenizer.decode([474, 270, 29880]))
print(tokenizer.decode([474, 270, 29880, 288, 1490, 29871, 236, 189, 169, 30948, 29881, 232, 141, 182, 29871, 236, 168, 152, 236, 167, 177, 1407, 1568, 270, 1289]))