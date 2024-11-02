import gradio as gr


def greet(code):
    print(code)
    return code


demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox")

demo.launch(share=True)