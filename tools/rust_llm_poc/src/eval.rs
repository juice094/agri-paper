use kalosm::language::*;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::io::Write;
use std::path::PathBuf;

#[derive(Debug, Clone, Deserialize)]
struct KbRecord {
    crop: String,
    disease: String,
    symptoms: String,
    treatment: String,
}

#[derive(Debug, Clone, Deserialize)]
struct BenchmarkRecord {
    id: String,
    crop: String,
    query: String,
    expected_disease: String,
    expected_keywords: Vec<String>,
    symptoms: String,
    treatment: String,
    #[serde(rename = "type")]
    _type: String,
    difficulty: String,
}

#[derive(Debug, Clone, Serialize)]
struct EvalResult {
    id: String,
    condition: String, // NoContext | CropOnly | Proposed
    query: String,
    expected_disease: String,
    context_disease: Option<String>,
    generated_answer: String,
    difficulty: String,
}

fn model_path() -> PathBuf {
    let seven = PathBuf::from(r"C:\Users\22414\Desktop\model\Qwen2.5-7B-Instruct.Q4_K_M.gguf");
    if seven.exists() {
        return seven;
    }
    PathBuf::from(r"C:\Users\22414\Desktop\model\Qwen2.5-14B-Instruct.Q4_K_M.gguf")
}

fn load_kb() -> anyhow::Result<Vec<KbRecord>> {
    let path = PathBuf::from(r"C:\Users\22414\Desktop\agri-paper\w3\engineer\agri_knowledge_base\agricultural_diseases_all.jsonl");
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

fn load_benchmark() -> anyhow::Result<Vec<BenchmarkRecord>> {
    let path = PathBuf::from(r"C:\Users\22414\Desktop\agri-paper\datasets\agri_qa_benchmark_extended.jsonl");
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

fn stratified_sample(records: &[BenchmarkRecord]) -> Vec<BenchmarkRecord> {
    use rand::seq::SliceRandom;
    use rand::SeedableRng;
    use rand::rngs::StdRng;

    let mut easy: Vec<_> = records.iter().filter(|r| r.difficulty == "easy").cloned().collect();
    let mut medium: Vec<_> = records.iter().filter(|r| r.difficulty == "medium").cloned().collect();
    let mut hard: Vec<_> = records.iter().filter(|r| r.difficulty == "hard").cloned().collect();

    let mut rng = StdRng::seed_from_u64(42);
    easy.shuffle(&mut rng);
    medium.shuffle(&mut rng);
    hard.shuffle(&mut rng);

    let mut sampled = Vec::with_capacity(80);
    sampled.extend(easy.into_iter().take(30));
    sampled.extend(medium.into_iter().take(30));
    sampled.extend(hard.into_iter().take(20));
    sampled.shuffle(&mut rng);
    sampled
}

fn tokenize(text: &str) -> HashSet<String> {
    text.to_lowercase()
        .split(|c: char| !c.is_alphabetic())
        .filter(|s| !s.is_empty())
        .map(|s| s.to_string())
        .collect()
}

fn retrieve_top1<'a>(query: &str, kb: &'a [KbRecord]) -> Option<&'a KbRecord> {
    let query_tokens = tokenize(query);
    let mut best: Option<(i32, &KbRecord)> = None;
    for rec in kb {
        let mut score = 0i32;
        let sym_tokens = tokenize(&rec.symptoms);
        score += query_tokens.intersection(&sym_tokens).count() as i32;
        if query.to_lowercase().contains(&rec.crop.to_lowercase()) {
            score += 10;
        }
        if score > 0 && best.as_ref().map_or(true, |(b, _)| score > *b) {
            best = Some((score, rec));
        }
    }
    best.map(|(_, r)| r)
}

fn build_system_prompt(base: &str, context: Option<String>) -> String {
    if let Some(ctx) = context {
        format!("{}\n\nRelevant context from the knowledge base:\n{}", base, ctx)
    } else {
        base.to_string()
    }
}

fn no_context(_query: &str, _kb: &[KbRecord]) -> Option<String> {
    None
}

fn crop_only(query: &str, kb: &[KbRecord]) -> Option<String> {
    let crop = kb.iter().find(|r| query.to_lowercase().contains(&r.crop.to_lowercase()))?;
    let ctx: String = kb
        .iter()
        .filter(|r| r.crop.to_lowercase() == crop.crop.to_lowercase())
        .map(|r| format!("- {} ({}): symptoms: {}; treatment: {}", r.crop, r.disease, r.symptoms, r.treatment))
        .collect::<Vec<_>>()
        .join("\n");
    Some(ctx)
}

fn proposed(query: &str, kb: &[KbRecord]) -> Option<String> {
    let rec = retrieve_top1(query, kb)?;
    Some(format!(
        "Crop: {}\nDisease: {}\nSymptoms: {}\nTreatment: {}",
        rec.crop, rec.disease, rec.symptoms, rec.treatment
    ))
}

async fn generate(model: &Llama, system_prompt: &str, query: &str) -> anyhow::Result<String> {
    let mut chat = model
        .chat()
        .with_system_prompt(system_prompt);

    let mut stream = chat(query);
    let mut answer = String::new();
    while let Some(token) = stream.next().await {
        answer.push_str(token.as_ref());
    }
    Ok(answer)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("agri-paper LLM Evaluation (kalosm)\n");

    let path = model_path();
    if !path.exists() {
        anyhow::bail!("Model not found at {}", path.display());
    }
    println!("Model: {}", path.display());

    let source = LlamaSource::new(FileSource::local(path));
    let model = Llama::builder()
        .with_source(source)
        .build()
        .await?;

    let kb = load_kb()?;
    let benchmark = load_benchmark()?;
    let sampled = stratified_sample(&benchmark);
    println!("Benchmark: {} total, sampled {} records\n", benchmark.len(), sampled.len());

    let base_prompt = "You are an agricultural expert. Help farmers diagnose crop diseases and provide integrated pest management advice in a concise, practical manner.";

    let conditions: Vec<(&str, fn(&str, &[KbRecord]) -> Option<String>)> = vec![
        ("NoContext", no_context),
        ("CropOnly", crop_only),
        ("Proposed", proposed),
    ];

    let timestamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let out_path = PathBuf::from(format!(
        r"C:\Users\22414\Desktop\agri-paper\w4\research\llm_eval_raw_{}.jsonl",
        timestamp
    ));
    let mut out_file = std::io::BufWriter::new(std::fs::File::create(&out_path)?);

    for (i, rec) in sampled.iter().enumerate() {
        for (cond_name, cond_fn) in &conditions {
            println!(
                "[{}/{}] {} | {} | {}",
                i + 1,
                sampled.len(),
                cond_name,
                rec.difficulty,
                rec.id
            );

            let context = cond_fn(&rec.query, &kb);
            let system_prompt = build_system_prompt(base_prompt, context.clone());
            let answer = generate(&model, &system_prompt, &rec.query).await?;

            let result = EvalResult {
                id: rec.id.clone(),
                condition: cond_name.to_string(),
                query: rec.query.clone(),
                expected_disease: rec.expected_disease.clone(),
                context_disease: context.as_ref().and_then(|_| retrieve_top1(&rec.query, &kb)).map(|r| r.disease.clone()),
                generated_answer: answer,
                difficulty: rec.difficulty.clone(),
            };

            serde_json::to_writer(&mut out_file, &result)?;
            out_file.write_all(b"\n")?;
        }
    }

    out_file.flush()?;
    println!("\nEvaluation complete. Results saved to: {}", out_path.display());
    Ok(())
}
