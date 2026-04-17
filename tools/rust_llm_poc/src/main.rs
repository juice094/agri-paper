use kalosm::language::*;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("============================================");
    println!("  agri-paper | Agricultural LLM REPL");
    println!("============================================");
    println!("Loading local Qwen2.5-14B-Instruct-GGUF via kalosm...");
    println!("Model path: C:\\Users\\22414\\Desktop\\model\\Qwen2.5-14B-Instruct.Q4_K_M.gguf\n");

    let source = LlamaSource::new(FileSource::local(
        "C:\\Users\\22414\\Desktop\\model\\Qwen2.5-14B-Instruct.Q4_K_M.gguf".into(),
    ));

    let model = Llama::builder()
        .with_source(source)
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
