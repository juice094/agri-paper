use kalosm::language::*;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("Rust LLM PoC for agri-paper");
    println!("This binary will load a local quantized model and generate answers for agricultural queries.");

    // Placeholder: actual model loading and inference will be implemented
    // once dependency compilation is verified.
    let model = Llama::builder()
        .with_source(LlamaSource::qwen_2_5_7b_instruct())
        .build()
        .await?;

    println!("Model loaded successfully.");

    let prompt = "What are the common symptoms of rice blast disease?";
    println!("\nPrompt: {prompt}\n");
    model(prompt).to_std_out().await?;
    Ok(())
}
