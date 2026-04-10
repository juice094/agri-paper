#!/usr/bin/env python3
"""Generate a 105-record agricultural QA benchmark from 15 seed records."""
import json
import random

SEED = [
    {"crop":"rice","disease":"Rice Blast","symptoms":"Diamond-shaped lesions on leaves, gray centers with brown margins, neck rot causing white heads","treatment":"Apply tricyclazole or azoxystrobin at tillering and booting stages; use resistant varieties; maintain proper spacing and avoid excessive nitrogen"},
    {"crop":"rice","disease":"Sheath Blight","symptoms":"Oval lesions on leaf sheaths near water line, gray-white centers with brown borders, lodging of plants","treatment":"Apply validamycin or hexaconazole; reduce plant density; improve field drainage; avoid excessive nitrogen fertilization"},
    {"crop":"rice","disease":"Bacterial Leaf Blight","symptoms":"Yellow to white lesions along leaf margins, wilting of seedlings, bacterial ooze on affected tissues","treatment":"Use resistant varieties; treat seeds with hot water; apply copper-based bactericides; practice crop rotation and field sanitation"},
    {"crop":"wheat","disease":"Powdery Mildew","symptoms":"White powdery patches on leaves and stems, yellowing and necrosis of infected tissue, stunted growth","treatment":"Apply triadimefon or propiconazole; use resistant cultivars; ensure adequate spacing for air circulation; avoid late nitrogen application"},
    {"crop":"wheat","disease":"Stripe Rust","symptoms":"Yellow-orange pustules arranged in stripes on leaves and stems, premature leaf senescence, reduced grain fill","treatment":"Apply tebuconazole or epoxiconazole at early detection; plant resistant varieties; monitor fields regularly in cool humid conditions"},
    {"crop":"wheat","disease":"Fusarium Head Blight","symptoms":"Bleached spikelets with pinkish fungal growth, shriveled grains with white chalky appearance, yield reduction","treatment":"Apply prothioconazole at flowering; practice crop rotation with non-cereals; bury crop residues; use moderately resistant varieties"},
    {"crop":"corn","disease":"Northern Corn Leaf Blight","symptoms":"Long elliptical gray-green lesions on leaves, severe defoliation under humid conditions, reduced photosynthesis","treatment":"Apply azoxystrobin or pyraclostrobin; use resistant hybrids; practice tillage to reduce residue; rotate crops with soybeans"},
    {"crop":"corn","disease":"Gray Leaf Spot","symptoms":"Rectangular tan to gray lesions bounded by leaf veins, severe blighting from lower canopy upward, yield loss","treatment":"Apply strobilurin or triazole fungicides; use resistant hybrids; manage residue through tillage; rotate with non-host crops"},
    {"crop":"corn","disease":"Corn Smut","symptoms":"Galls on ears, tassels, leaves, and stalks, galls rupture releasing black spores, cosmetic and yield damage","treatment":"Remove and destroy galls before rupture; use resistant hybrids; avoid mechanical injury to plants; practice crop rotation"},
    {"crop":"citrus","disease":"Citrus Canker","symptoms":"Raised corky lesions on leaves fruit and twigs, yellow halos around lesions, premature fruit drop and defoliation","treatment":"Apply copper sprays during flush growth; prune infected twigs; use windbreaks to reduce spread; plant canker-free nursery stock"},
    {"crop":"citrus","disease":"Huanglongbing (Citrus Greening)","symptoms":"Blotchy mottle on leaves, lopsided bitter fruit with aborted seeds, twig dieback, tree decline","treatment":"No cure available; remove infected trees; control Asian citrus psyllid vector with insecticides; use certified disease-free planting material"},
    {"crop":"citrus","disease":"Greasy Spot","symptoms":"Yellow-brown blisters on lower leaf surface, black velvety lesions, premature defoliation and fruit drop","treatment":"Apply petroleum oil or copper fungicides in summer; improve orchard air circulation; remove fallen leaves to reduce inoculum"},
    {"crop":"tomato","disease":"Early Blight","symptoms":"Dark brown concentric rings on lower leaves, yellowing around lesions, stem cankers at soil line, fruit rot","treatment":"Apply chlorothalonil or mancozeb; mulch to reduce soil splash; stake plants for air circulation; rotate with non-solanaceous crops"},
    {"crop":"tomato","disease":"Late Blight","symptoms":"Water-soaked dark lesions on leaves and stems, white fungal growth on undersides in humid conditions, fruit rot","treatment":"Apply mandipropamid or cymoxanil protectively; destroy infected plant debris; ensure good drainage; use resistant varieties where available"},
    {"crop":"tomato","disease":"Tomato Yellow Leaf Curl Virus","symptoms":"Upward curling and yellowing of leaf margins, stunted growth, reduced flowering and fruit set, plant dwarfing","treatment":"Use resistant varieties; control whitefly vectors with insecticides and reflective mulches; remove infected plants; use virus-free transplants"},
]

def make_templates(record, idx):
    c, d, s, t = record["crop"], record["disease"], record["symptoms"], record["treatment"]
    templates = [
        {
            "query": f"My {c} shows {s.split(',')[0].lower()}. What disease could this be?",
            "type": "diagnosis_from_first_symptom",
            "difficulty": "easy",
        },
        {
            "query": f"I observed {s.lower()} on my {c}. How should I manage it?",
            "type": "diagnosis_and_management",
            "difficulty": "medium",
        },
        {
            "query": f"What are the typical symptoms of {d} in {c}?",
            "type": "symptom_recognition",
            "difficulty": "easy",
        },
        {
            "query": f"Which treatment options are recommended for {d} affecting {c}?",
            "type": "treatment_recall",
            "difficulty": "easy",
        },
        {
            "query": f"A farmer reports {s.split(',')[1].strip().lower()} and {s.split(',')[2].strip().lower()} in a {c} field. Diagnose the disease and suggest control measures.",
            "type": "multi_symptom_diagnosis",
            "difficulty": "medium",
        },
        {
            "query": f"How can I prevent or treat {d} in {c} cultivation?",
            "type": "prevention_and_treatment",
            "difficulty": "medium",
        },
        {
            "query": f"In the field, {c.lower()} plants exhibit {s.lower()}. Provide a diagnosis and actionable recommendations.",
            "type": "field_observation",
            "difficulty": "hard",
        },
    ]
    results = []
    for i, tmpl in enumerate(templates):
        qid = f"agri_qa_{idx:03d}_{i}"
        # Extract a few keyword spans from treatment for automated scoring
        keywords = [kw.strip().lower() for kw in t.split(";")[:2]]
        results.append({
            "id": qid,
            "crop": c,
            "query": tmpl["query"],
            "expected_disease": d,
            "expected_keywords": keywords,
            "symptoms": s,
            "treatment": t,
            "type": tmpl["type"],
            "difficulty": tmpl["difficulty"],
        })
    return results

def main():
    random.seed(42)
    records = []
    for idx, r in enumerate(SEED):
        records.extend(make_templates(r, idx))
    with open("agri_qa_benchmark.jsonl", "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Generated {len(records)} QA records -> agri_qa_benchmark.jsonl")

if __name__ == "__main__":
    main()
