![Tiktokenizer](https://user-images.githubusercontent.com/1443449/222597674-287aefdc-f0e1-491b-9bf9-16431b1b8054.svg)

***
# fork 后改动说明

支持使用 python 自定义编码方法，在`py_server/encoders`下新建 python 包并实现 encode 函数即可

## 简易使用

1. 解压 `out.tar.gz`，生成 out 文件夹

    `tar -xzf out.tar.gz`

2. cd 到 py_server 下

    初次使用请根据 requirements.txt 补全依赖

    执行 `python3 app.py --port=xxxx --ip=xxxx` 即可

## 添加自定义 encoder
复制 `py_server/encoders/demo_lamma` 并重命名，阅读下实现，如果同样使用 sentencepiece，可能只需替换 `tokenizer.model`

# Tiktokenizer

Online playground for `openai/tiktoken`, calculating the correct number of tokens for a given prompt.

Special thanks to [Diagram](https://diagram.com/) for sponsorship and guidance.

https://user-images.githubusercontent.com/1443449/222598119-0a5a536e-6785-44ad-ba28-e26e04f15163.mp4

## Acknowledgments

- [T3 Stack](https://create.t3.gg/)
- [shadcn/ui](https://github.com/shadcn/ui)
- [openai/tiktoken](https://github.com/openai/tiktoken)

