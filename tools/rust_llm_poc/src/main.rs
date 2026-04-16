use kalosm::language::*;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("============================================");
    println!("  agri-paper | Agricultural LLM REPL");
    println!("============================================");
    println!("Loading Qwen2.5-7B-Instruct via kalosm...");
    println!("(First run may download ~4.5 GB from HuggingFace)\n");

    let model = Llama::builder()
        .with_source(LlamaSource::qwen_2_5_7b_instruct())
        .build()
        .await?;

    println!("Model ready. Type an agricultural question below.");
    println!("Commands: 'exit' or 'quit' to stop.\n");

    let stdin = std::io::stdin();
    let mut buffer = String::new();

    loop {
        print!("> ");
        std::io::Write::flush(&mut std::io::stdout())?;

        buffer.clear();
        stdin.read_line(&mut buffer)?;
        let input = buffer.trim();

        if input.is_empty() {
            continue;
        }
        if input.eq_ignore_ascii_case("exit") || input.eq_ignore_ascii_case("quit") {
            println!("Goodbye!");
            break;
        }

        println!("\n[Assistant]:");
        model(input).to_std_out().await?;
        println!("\n");
    }

    Ok(())
}
