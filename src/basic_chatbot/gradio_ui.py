import gradio as gr
    
def chat_interface(bot) -> gr.Blocks: 
    """Creates a UI for the chatbot using Gradio."""
    def clear_chat():
        if hasattr(bot, "clear_chat"):
            bot.clear_chat()
        return [], ""

    def get_reponse(m, h):
        return bot.respond(m, h), ""

    with gr.Blocks() as demo:
        gr.Markdown("MyAssistant")
        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox(label="Message")

        msg.submit(
            get_reponse,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg],
        )

        clear_btn = gr.ClearButton([chatbot, msg])
        clear_btn.click(
            fn=clear_chat,
            inputs=[],
            outputs=[chatbot, msg],
        )

    return demo