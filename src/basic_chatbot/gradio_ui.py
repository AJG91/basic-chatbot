import gradio as gr
    
def chat_interface(bot) -> gr.Blocks:
    def clear_chat():
        if hasattr(bot, "clear_chat"):
            bot.clear_chat()
        return [], ""

    with gr.Blocks() as demo:
        gr.Markdown("MyAssistant")
        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox(label="Message")

        msg.submit(
            lambda m, h: bot.respond(m, h),
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )

        clear_btn = gr.ClearButton([chatbot, msg])
        clear_btn.click(
            fn=clear_chat,
            inputs=[],
            outputs=[chatbot, msg],
        )

    return demo