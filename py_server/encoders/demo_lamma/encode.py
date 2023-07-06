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

def conv(tokens, text):
    '''
    decode 每个解析出的 int token，然后找到原始字符串中对应的字符，打包成 Segments List
    某些 emoji 或者汉字会使用多个 token 来表示，需要另外处理

    type Segments = { text: string; tokens: { id: number; idx: number }[] }[]
    '''
    segments = []
    token_acc = []
    for idx in range(len(tokens)):
    
        token_acc.append({'id':tokens[idx], 'idx':idx})
        decoded = tokenizer.decode([x['id'] for x in token_acc])
        
        # 如果下一个字符是空格，但 decode 结果并不是空格开头，给 decode 补空格去做尝试
        got = [' ' + decoded, decoded] if len(text) and text[0] == ' ' \
            else [decoded]
        
        hit = False
        for tk in got:
            if hit:
                continue
            tk_len = len(tk)
            # 某些 emoji 或者汉字会使用多个 token 来表示
            # 解析结果与原始字符串相同时，塞入一个结果，否则继续 append 导 token_acc
            txt_to_check = text[:tk_len]
            if tk == txt_to_check:
                segments.append({
                    'text': txt_to_check,
                    'tokens': token_acc.copy()
                })
                text = text[tk_len:]
                token_acc = []
                hit = True

    return segments

def encode(text):
    ids = tokenizer.encode(text, False, False)
    return conv(ids, text)
    
if __name__=='__main__':

    def test(text:str):
        result = "".join([seg['text'] for seg in encode(text)])
        print(text)
        print(result)
        assert text==result
        print('------')

    test(' ')
    test('1')
    test('a')
    test('apple')
    test('apple apple apple')
    test('咚咚咚咚')
    test('在')
    test('饕餮')
    test('one two three')
    test(' 😃 one two three ')
    test('😃咚咚咚噢的那个 one two three ')
    test(' one two three\n ThreeThree😃Three')
    
