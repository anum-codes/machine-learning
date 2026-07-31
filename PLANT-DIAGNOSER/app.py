"""Gradio presentation layer serving the updated ML application."""

import gradio as gr
import config
from model_service import PlantDiagnosticEngine

engine = PlantDiagnosticEngine()

def ui_handler(input_image):
    result = engine.predict(input_image)
    if result["status"] == "error":
        return f"🚨 Error: {result['message']}"
        
    label = result["label"]
    confidence = result["confidence"]
    
    # Check if the result indicates the plant is healthy
    if "healthy" in label.lower():
        return (
            f"🌿 DIAGNOSIS: {label}\n"
            f"📊 CONFIDENCE: {confidence:.1f}%\n"
            f"✅ STATUS: Healthy Foliage\n"
            f"📋 RECOMMENDATION: Keep doing what you're doing!"
        )
    else:
        return (
            f"🍂 DIAGNOSIS: {label}\n"
            f"📊 CONFIDENCE: {confidence:.1f}%\n"
            f"⚠️ STATUS: Disease/Pathogen Detected\n"
            f"📋 RECOMMENDATION: Research treatment for {label}. Consider pruning infected leaves to protect the rest of the crop."
        )

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍂 Enterprise Plant Health Diagnoser")
    gr.Markdown("An automated computer vision inference tool for analyzing foliage and detecting health status.")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="Upload Leaf Sample")
            submit_btn = gr.Button("Execute Analysis", variant="primary")
        with gr.Column():
            text_output = gr.Textbox(label="Diagnostic Report", interactive=False, lines=6)
            
    submit_btn.click(fn=ui_handler, inputs=image_input, outputs=text_output)

if __name__ == "__main__":
    demo.launch(server_name=config.SERVER_NAME, server_port=config.SERVER_PORT)