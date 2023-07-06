![Tiktokenizer](https://user-images.githubusercontent.com/1443449/222597674-287aefdc-f0e1-491b-9bf9-16431b1b8054.svg)

***
# fork 后改动说明

支持使用 python 自定义编码方法，在`py_server/encoders`下新建 python 包并实现 encode 函数即可

## 简易使用

1. 解压 `out.tar.gz`，释放编译好的前端组件，生成 out 文件夹

    ```
    tar -xzf out.tar.gz
    ```

2. cd 到 py_server 下

    初次使用请安装依赖

    推荐使用新的 venv
    ```
    cd py_server
    pip install -r requirements.txt
    python3 app.py --port=xxxx --host=xxxx
    ```
    默认 ip `0.0.0.0`, 端口 `8231`
    
    浏览器访问该地址即可

    

## 添加自定义 encoder

复制 `py_server/encoders/demo_llama` 并重命名，
请阅读下实现，重写并导出 `encode` 函数即可

如果同样使用 sentencepiece，可能只需替换 `tokenizer.model`

新增 encoder 路径后刷新页面即可在列表中出现

如果在原位开发编辑，建议重启服务进程来刷新

---


# Tiktokenizer

Online playground for `openai/tiktoken`, calculating the correct number of tokens for a given prompt.

Special thanks to [Diagram](https://diagram.com/) for sponsorship and guidance.

https://user-images.githubusercontent.com/1443449/222598119-0a5a536e-6785-44ad-ba28-e26e04f15163.mp4

## Acknowledgments

- [T3 Stack](https://create.t3.gg/)
- [shadcn/ui](https://github.com/shadcn/ui)
- [openai/tiktoken](https://github.com/openai/tiktoken)

