use kalosm::language::*;
use serde::Deserialize;
use std::collections::HashSet;
use std::path::PathBuf;

#[derive(Debug, Clone, Deserialize)]
struct Record {
    crop: String,
    disease: String,
    symptoms: String,
    treatment: String,
}

fn model_path() -> PathBuf {
    let seven = PathBuf::from(r"C:\Users\22414\Desktop\model\Qwen2.5-7B-Instruct.Q4_K_M.gguf");
    if seven.exists() {
        println!("Using 7B model (Qwen2.5-7B-Instruct-Q4_K_M.gguf)\n");
        return seven;
    }
    let fourteen = PathBuf::from(r"C:\Users\22414\Desktop\model\Qwen2.5-14B-Instruct.Q4_K_M.gguf");
    println!("Using 14B model (Qwen2.5-14B-Instruct.Q4_K_M.gguf)\n");
    fourteen
}

fn kb_path() -> PathBuf {
    PathBuf::from(r"C:\Users\22414\Desktop\agri-paper\w3\engineer\agri_knowledge_base\agricultural_diseases_all.jsonl")
}

fn load_kb() -> anyhow::Result<Vec<Record>> {
    let path = kb_path();
    let content = std::fs::read_to_string(&path)?;
    let mut records = Vec::new();
    for line in content.lines() {
        if line.trim().is_empty() {
            continue;
        }
        records.push(serde_json::from_str(line)?);
    }
    Ok(records)
}

fn tokenize(text: &str) -> HashSet<String> {
    text.to_lowercase()
        .split(|c: char| !c.is_alphabetic())
        .filter(|s| !s.is_empty())
        .map(|s| s.to_string())
        .collect()
}

fn retrieve_top1<'a>(query: &str, kb: &'a [Record]) -> Option<&'a Record> {
    let query_tokens = tokenize(query);
    let mut best: Option<(i32, &Record)> = None;
    for rec in kb {
        let mut score = 0i32;
        let sym_tokens = tokenize(&rec.symptoms);
        let overlap: i32 = query_tokens.intersection(&sym_tokens).count() as i32;
        score += overlap;
        if query.to_lowercase().contains(&rec.crop.to_lowercase()) {
            score += 10;
        }
        if score > 0 {
            if best.as_ref().map_or(true, |(b, _)| score > *b) {
                best = Some((score, rec));
            }
        }
    }
    best.map(|(_, r)| r)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("============================================");
    println!("  agri-paper | Agricultural LLM REPL");
    println!("============================================");
    println!("Loading local model via kalosm...");

    let path = model_path();
    if !path.exists() {
        anyhow::bail!("Model not found at {}", path.display());
    }

    let source = LlamaSource::new(FileSource::local(path));
    let model = Llama::builder()
        .with_source(source)
        .build()
        .await?;

    let kb = load_kb()?;
    println!("Knowledge base loaded: {} records\n", kb.len());

    let base_prompt = "You are an agricultural expert. Help farmers diagnose crop diseases and provide integrated pest management advice in a concise, practical manner.";

    println!("Model ready. Type an agricultural question below.");
    println!("Commands: 'exit' or 'quit' to stop.\n");

    let stdin = std::io::stdin();
    let mut buffer = String::new();

    loop {
        print!("> ");
        std::io::Write::flush(&mut std::io::stdout())?;

        buffer.clear();
        if stdin.read_line(&mut buffer)? == 0 {
            break;
        }
        let input = buffer.trim();

        if input.is_empty() {
            continue;
        }
        if input.eq_ignore_ascii_case("exit") || input.eq_ignore_ascii_case("quit") {
            println!("Goodbye!");
            break;
        }

        let rec = retrieve_top1(input, &kb);
        let system_prompt = if let Some(r) = rec {
            format!(
                "{}\n\nRelevant context from the knowledge base:\nCrop: {}\nDisease: {}\nSymptoms: {}\nTreatment: {}",
                base_prompt, r.crop, r.disease, r.symptoms, r.treatment
            )
        } else {
            base_prompt.to_string()
        };

        let mut chat = model
            .chat()
            .with_system_prompt(&system_prompt);

        println!("\n[Assistant]:");
        chat(input).to_std_out().await?;
        println!("\n");
    }

    Ok(())
}
