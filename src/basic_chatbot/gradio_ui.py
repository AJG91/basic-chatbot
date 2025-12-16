import gradio as gr
    
def build_demo(bot) -> gr.Blocks:

    with gr.Blocks() as demo:
        gr.Markdown("Chatbot")
        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox(label="Message")

        msg.submit(
            lambda m, h: bot.respond(m, h),
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )

    return demo