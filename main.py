import gradio as gr
import asyncio
import logging

from agents import Runner, trace
from src.lms_agents.auth import auth_agent
from src.lms_agents.manager.manager_agent import ManagerAgent

logger = logging.getLogger(__name__)

# Initialize agent once
manager_agent = ManagerAgent()


async def agent_reply(message, history):
    try:
        with trace("User Assistant Session"):
            result = await Runner.run(
                manager_agent.agent,
                message,
                max_turns=50,
            )
            return result.final_output or "❌ No response generated"
    except Exception as e:
        logger.error(f"Error in agent reply: {e}")
        return f"❌ Application failed: {e}"


def chat(message, history):
    return asyncio.run(agent_reply(message, history))


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="container"):
        gr.Markdown(
            """
            <div style='text-align: center; font-size: 28px; font-weight: bold; padding: 10px;'>
                💬 Manager Agent Chat
            </div>
            <p style='text-align: center; font-size: 16px; color: gray; margin-bottom: 20px;'>
                Interactive assistant demo
            </p>
            """
        )

        chatbot = gr.Chatbot(
            label="Conversation",
            bubble_full_width=False,
            show_copy_button=True,
            height=500,
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message...",
                lines=1,
                scale=4,
                autofocus=True,
                container=False,
            )
            send = gr.Button("🚀 Send", scale=1)
        clear = gr.Button("🗑️ Clear Chat", variant="stop")

    def user_submit(user_message, history):
        history = history + [(user_message, chat(user_message, history))]
        return "", history

    msg.submit(user_submit, [msg, chatbot], [msg, chatbot])
    send.click(user_submit, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo.launch()
