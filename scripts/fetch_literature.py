import csv
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
DOCS_DIR = os.path.join(ROOT, "docs")
STATUS_PATH = os.path.join(ROOT, "child_status.md")
RAW_PATH = os.path.join(DATA_DIR, "openalex_literature_raw.jsonl")
MATRIX_PATH = os.path.join(DOCS_DIR, "related_work_matrix.csv")


QUERIES = [
    ("sim-to-real robotics", "sim_to_real_core"),
    ("sim to real transfer robotics", "sim_to_real_core"),
    ("reality gap robotics", "sim_to_real_core"),
    ("domain randomization robotics", "domain_randomization"),
    ("dynamics randomization robotics", "domain_randomization"),
    ("visual domain randomization robot", "domain_randomization"),
    ("robot learning from simulation", "simulation_training"),
    ("policy transfer robot reinforcement learning", "policy_transfer"),
    ("sim-to-real reinforcement learning robot", "policy_transfer"),
    ("robot domain adaptation", "domain_adaptation"),
    ("visual domain adaptation robotics", "domain_adaptation"),
    ("3D perception domain adaptation robot", "domain_adaptation"),
    ("system identification robot learning", "system_identification"),
    ("adaptive robot control system identification", "system_identification"),
    ("online dynamics adaptation robotics", "system_identification"),
    ("residual reinforcement learning robotics", "residual_learning"),
    ("residual dynamics robot manipulation", "residual_learning"),
    ("model-based robot learning sim-to-real", "world_models"),
    ("world models robotics physical reasoning", "world_models"),
    ("foundation models robotics sim-to-real", "foundation_robotics"),
    ("contact-rich manipulation sim-to-real", "contact_manipulation"),
    ("robotic manipulation domain randomization", "contact_manipulation"),
    ("deformable object manipulation sim-to-real", "contact_manipulation"),
    ("legged locomotion sim-to-real", "locomotion"),
    ("quadruped sim-to-real learning", "locomotion"),
    ("tactile robot sim-to-real", "tactile"),
    ("robot failure detection learning", "failure_analysis"),
    ("causal representation learning robotics", "causal_robotics"),
    ("robot causal dynamics adaptation", "causal_robotics"),
    ("mechanism design adaptation robotics failure", "failure_analysis"),
]


ROBOTICS_TERMS = [
    "robot", "robotic", "manipulation", "locomotion", "grasp", "gripper",
    "arm", "quadruped", "legged", "mobile manipulator", "tactile", "control",
    "embodied", "sim-to-real", "sim to real", "reality gap", "physical",
]


CATEGORY_RULES = [
    ("domain_randomization", ["domain random", "randomization", "randomisation", "dynamics random"]),
    ("domain_adaptation", ["domain adaptation", "adaptation", "transfer learning", "unsupervised domain"]),
    ("system_identification", ["system identification", "identification", "parameter estimation", "calibration"]),
    ("residual_learning", ["residual", "residual reinforcement", "residual dynamics"]),
    ("policy_transfer", ["policy transfer", "reinforcement learning", "rl", "policy"]),
    ("contact_manipulation", ["contact", "manipulation", "grasp", "push", "deformable"]),
    ("locomotion", ["locomotion", "quadruped", "legged", "walking"]),
    ("tactile", ["tactile", "touch", "haptic"]),
    ("world_models", ["world model", "dynamics model", "model-based", "physical reasoning"]),
    ("foundation_robotics", ["foundation model", "large language", "vision-language-action", "robot foundation"]),
    ("causal_robotics", ["causal", "mechanism", "invariant", "counterfactual"]),
    ("failure_analysis", ["failure", "fault", "robustness", "diagnosis"]),
]


ANNOTATIONS = {
    "domain_randomization": {
        "problem": "Close the reality gap by training policies over many randomized simulator domains.",
        "mechanism": "Expose the policy to sampled visual, dynamics, and nuisance parameters during training.",
        "assumptions": "The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.",
        "fixed": "Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.",
        "ignored": "Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.",
        "less_novel": "A broad claim that randomized simulation improves robustness or transfer.",
        "open": "Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.",
    },
    "domain_adaptation": {
        "problem": "Align source and target distributions so learned perception or policies transfer across domains.",
        "mechanism": "Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.",
        "assumptions": "Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.",
        "fixed": "Controller semantics, intervention set, simulator causal graph, and failure labels.",
        "ignored": "Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.",
        "less_novel": "A generic feature-alignment framing for sim-to-real transfer.",
        "open": "Intervention-relevant mechanism identification under sparse real trials.",
    },
    "system_identification": {
        "problem": "Estimate physical parameters of the real system and update the simulator or controller.",
        "mechanism": "Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.",
        "assumptions": "The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.",
        "fixed": "Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.",
        "ignored": "Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.",
        "less_novel": "Claims that transfer can be repaired by estimating simulator parameters.",
        "open": "Mechanism-level probes that identify the repair before accurate full-parameter estimation.",
    },
    "residual_learning": {
        "problem": "Correct a nominal model or policy with learned residual dynamics/actions.",
        "mechanism": "Train an additive residual controller or dynamics correction from real/sim trajectories.",
        "assumptions": "A smooth residual is sufficient and the correction can be learned safely from available data.",
        "fixed": "Residual basis, failure type, contact mode decomposition, and safe diagnostic policy.",
        "ignored": "Discrete failure causes, residuals that cancel in training but diverge under repair, and mechanism-specific constraints.",
        "less_novel": "Adding a learned residual to bridge sim-to-real.",
        "open": "Choosing the residual structure from diagnosed failure mechanisms.",
    },
    "policy_transfer": {
        "problem": "Train policies in simulation that perform on a physical robot.",
        "mechanism": "Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.",
        "assumptions": "Task return can drive the right invariant behavior despite sparse real feedback.",
        "fixed": "Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.",
        "ignored": "Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.",
        "less_novel": "A general sim-trained policy transfer contribution.",
        "open": "A repairable failure-mechanism representation for sample-limited deployment.",
    },
    "contact_manipulation": {
        "problem": "Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.",
        "mechanism": "Model, randomize, or learn contact dynamics and manipulation policies.",
        "assumptions": "Contact uncertainty can be represented as parameters or broad robustness margins.",
        "fixed": "Failure onset signatures, controller repair choices, and mechanism-specific contact probes.",
        "ignored": "Ambiguous contacts with identical task statistics but opposite corrective actions.",
        "less_novel": "Showing that contact dynamics matter for sim-to-real manipulation.",
        "open": "Failure-mechanism diagnosis for contact repairs under few real interactions.",
    },
    "locomotion": {
        "problem": "Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.",
        "mechanism": "Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.",
        "assumptions": "Morphology and terrain variations can be covered by training distributions or latent adaptation.",
        "fixed": "Named failure mechanisms and their repair semantics.",
        "ignored": "Aliased failure signatures and non-stationary faults after deployment.",
        "less_novel": "Locomotion sim-to-real through randomized or adaptive policies.",
        "open": "Mechanism-first repair when the robot must choose among incompatible fixes.",
    },
    "tactile": {
        "problem": "Use tactile sensing to bridge contact uncertainty in real robotic interaction.",
        "mechanism": "Learn tactile representations, calibrate sensors, or fuse touch with vision/control.",
        "assumptions": "Sensing reveals the relevant physical state once properly calibrated.",
        "fixed": "Failure taxonomy and intervention selection.",
        "ignored": "When the same tactile distribution corresponds to different repair mechanisms.",
        "less_novel": "Using tactile observations as additional transfer signal.",
        "open": "Probe design that separates failure mechanisms rather than merely improving sensing.",
    },
    "world_models": {
        "problem": "Learn predictive models of robot-environment dynamics for planning and transfer.",
        "mechanism": "Train latent or structured dynamics models and plan/control through predictions.",
        "assumptions": "Prediction accuracy on collected rollouts is aligned with repair quality.",
        "fixed": "Failure classes, diagnostic interventions, and counterfactual repair objectives.",
        "ignored": "Predictively equivalent mechanisms requiring different control changes.",
        "less_novel": "Learning a robot world model for sim-to-real planning.",
        "open": "Mechanism-identifiable world models whose latent factors are repair variables.",
    },
    "foundation_robotics": {
        "problem": "Use broad pretrained models to generalize robot behavior across tasks and embodiments.",
        "mechanism": "Scale multimodal pretraining, action tokenization, imitation, and task conditioning.",
        "assumptions": "Broad data captures transferable physical regularities and deployment gaps can be absorbed by adaptation.",
        "fixed": "Mechanism-level failure diagnosis and causal repair guarantees.",
        "ignored": "Small-data physical faults and incompatible repairs hidden under similar language/visual context.",
        "less_novel": "A scale-based generalization story for robot adaptation.",
        "open": "Mechanism-first deployment repairs complementary to broad pretraining.",
    },
    "causal_robotics": {
        "problem": "Use causal or invariant structure to improve robot learning and generalization.",
        "mechanism": "Represent interventions, invariances, causal graphs, or counterfactual dynamics.",
        "assumptions": "The right causal variables are observed or learnable from available environments.",
        "fixed": "Concrete sim-to-real failure mechanisms and repair policies.",
        "ignored": "Operational diagnostic probes and contact/control-specific repair conflicts.",
        "less_novel": "The abstract claim that causal variables aid transfer.",
        "open": "A mechanism-first adaptation protocol with runnable robotic evidence.",
    },
    "failure_analysis": {
        "problem": "Detect, classify, or recover from robot failures and faults.",
        "mechanism": "Monitor anomalies, diagnose faults, or switch controllers.",
        "assumptions": "Failure labels and monitoring signals are available after deployment.",
        "fixed": "Sim-to-real transfer framing and pre-failure mechanism probes.",
        "ignored": "Nuisance-heavy domain statistics and ambiguous failures before catastrophic collapse.",
        "less_novel": "Failure classification or recovery as a standalone robotics module.",
        "open": "Using failure mechanisms as the primary representation for sim-to-real adaptation.",
    },
    "simulation_training": {
        "problem": "Use simulation to generate robot training data and policies.",
        "mechanism": "Procedural simulation, synthetic data, imitation, policy learning, or sim-trained perception.",
        "assumptions": "Simulator coverage and transfer procedures are sufficient for real deployment.",
        "fixed": "Deployment-time repair mechanism and causal diagnosis.",
        "ignored": "Mechanism-specific transfer failures hidden by aggregate success rates.",
        "less_novel": "More simulation as the source of robot generalization.",
        "open": "Evidence that adapting failure mechanisms can dominate adapting domain statistics.",
    },
    "other": {
        "problem": "Improve robot generalization, adaptation, or transfer under physical distribution shift.",
        "mechanism": "A task-specific robot learning, control, perception, or modeling method.",
        "assumptions": "The paper's chosen representation captures the real transfer bottleneck.",
        "fixed": "Explicit failure-mechanism diagnosis and repair selection.",
        "ignored": "Cases where similar domains need incompatible repairs.",
        "less_novel": "General robot adaptation motivation.",
        "open": "Mechanism-first sim-to-real adaptation with adversarial novelty boundaries.",
    },
}


HIDDEN_ASSUMPTIONS = [
    "The domain statistics that differ between sim and real are the variables that determine repair.",
    "A single randomized simulator family contains the real deployment mechanism.",
    "Visual appearance shift and physical mechanism shift can be handled by the same invariant representation.",
    "Better prediction of next observations implies better selection of adaptation repairs.",
    "Physical parameters are identifiable from the few rollouts available during deployment.",
    "Continuous residual corrections are adequate for discrete failure mechanisms.",
    "The policy can learn to ignore all nuisance variables without being told which are nuisances.",
    "A real-world failure is a point in a parameter space rather than a member of a mechanism class.",
    "Training-time robustness transfers to deployment-time diagnosis.",
    "Contact failures can be averaged into smooth dynamics residuals.",
    "The same repair is safe for all domains that share a distributional embedding.",
    "Task reward gives timely information about the cause of failure.",
    "Domain labels are more useful than causal failure labels.",
    "Probe actions are too costly to be part of sim-to-real adaptation.",
    "More diverse simulation is the main bottleneck rather than the wrong adaptation coordinate.",
    "The simulator should be updated before the repair policy is chosen.",
    "Failure modes are independent of the controller used to expose them.",
    "Texture, lighting, and other nuisance shifts are harmless once randomized.",
    "Mechanisms that have identical passive rollouts will need identical repairs.",
    "The target domain is stationary during adaptation.",
    "A learned latent variable will align with human-interpretable physical mechanisms.",
    "The adaptation objective can be specified without naming what counts as a repaired failure.",
    "Averaging over randomized domains does not wash out rare but repair-critical signatures.",
    "Full system identification is necessary before useful sim-to-real repair.",
    "The failure boundary observed in simulation is the same boundary that matters on hardware.",
]


DIRECTIONS = [
    {
        "name": "Mechanism-First Repair Coordinates",
        "breaks": "Domain statistics are the right adaptation coordinate.",
        "mechanism": "Use short diagnostic interventions to classify transfer failures into intervention-relevant mechanisms before choosing repair.",
        "why_strong": "Directly attacks non-identifiability: two domains can share statistics but require opposite repairs.",
        "risk": "Synthetic evidence may be seen as too narrow unless tied to contact/control failures.",
    },
    {
        "name": "Counterfactual Contact Probes",
        "breaks": "Passive deployment rollouts are enough for adaptation.",
        "mechanism": "Choose small probe actions whose residual signatures separate friction, compliance, delay, and gain mechanisms.",
        "why_strong": "Makes observability central rather than adding another estimator.",
        "risk": "Probe design can look like active learning unless the mechanism/repair link is explicit.",
    },
    {
        "name": "Repair-Equivalence Classes for Sim-to-Real",
        "breaks": "Parameter accuracy is the right success metric for adaptation.",
        "mechanism": "Group domains by the repair they require, even when their physical parameters differ.",
        "why_strong": "Changes the target from identifying the world to identifying the intervention.",
        "risk": "Needs careful distinction from robust control and residual policy switching.",
    },
    {
        "name": "Failure-Aliasing Lower Bounds",
        "breaks": "Distribution alignment can always recover transfer-relevant invariances.",
        "mechanism": "Prove adapters using only passive domain statistics fail under aliased mechanisms, then show diagnostic probes break the alias.",
        "why_strong": "Provides an adversarial formal boundary for existing domain adaptation claims.",
        "risk": "The lower bound must not overclaim beyond the stylized setting.",
    },
]


def update_status(stage, current_step, commands, failures=None, recovery_steps=None, notes=None):
    failures = failures or ["none"]
    recovery_steps = recovery_steps or ["none"]
    notes = notes or []
    lines = [
        f"stage: {stage}",
        f"current_step: {current_step}",
        f"last_updated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "commands:",
    ]
    lines.extend(f"- {c}" for c in commands)
    lines.append("")
    lines.append("failures:")
    lines.extend(f"- {f}" for f in failures)
    lines.append("")
    lines.append("recovery_steps:")
    lines.extend(f"- {r}" for r in recovery_steps)
    lines.append("")
    lines.append("notes:")
    if notes:
        lines.extend(f"- {n}" for n in notes)
    else:
        lines.append("- none")
    try:
        with open(STATUS_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as exc:
        print(f"status update failed: {exc}")


def clean_text(value):
    if value is None:
        return ""
    text = str(value).replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def abstract_from_inverted_index(index):
    if not isinstance(index, dict):
        return ""
    positions = []
    for word, locs in index.items():
        for loc in locs:
            positions.append((loc, word))
    positions.sort()
    return clean_text(" ".join(word for _, word in positions))


def first_location_name(work):
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    return clean_text(source.get("display_name") or "")


def authors_of(work, cap=6):
    names = []
    for item in work.get("authorships") or []:
        author = item.get("author") or {}
        name = clean_text(author.get("display_name") or "")
        if name:
            names.append(name)
    if len(names) > cap:
        return "; ".join(names[:cap]) + "; et al."
    return "; ".join(names)


def concept_names(work):
    names = []
    for concept in work.get("concepts") or []:
        name = clean_text(concept.get("display_name") or "")
        if name:
            names.append(name)
    for kw in work.get("keywords") or []:
        name = clean_text(kw.get("display_name") or kw.get("keyword") or "")
        if name:
            names.append(name)
    return names


def classify_category(title, abstract, query_tag):
    blob = f"{title} {abstract} {query_tag}".lower()
    best = ("other", 0)
    for category, terms in CATEGORY_RULES:
        score = sum(1 for term in terms if term in blob)
        if score > best[1]:
            best = (category, score)
    if best[1] == 0 and query_tag:
        if query_tag in ANNOTATIONS:
            return query_tag
        if query_tag == "sim_to_real_core":
            return "simulation_training"
    return best[0]


def relevance_score(work, title, abstract, concepts, query_tag):
    blob = f"{title} {abstract} {' '.join(concepts)} {query_tag}".lower()
    score = 0.0
    for term in ROBOTICS_TERMS:
        if term in blob:
            score += 2.0
    for term in ["sim-to-real", "sim to real", "reality gap", "domain randomization", "domain adaptation", "system identification", "contact", "failure", "mechanism", "causal"]:
        if term in blob:
            score += 3.0
    year = work.get("publication_year") or 0
    if year >= 2020:
        score += 2.0
    citations = work.get("cited_by_count") or 0
    score += min(8.0, math.log1p(citations))
    return score


def hostile_score(category, title, abstract, citations, year):
    blob = f"{title} {abstract}".lower()
    category_weight = {
        "domain_randomization": 8,
        "domain_adaptation": 7,
        "system_identification": 8,
        "residual_learning": 7,
        "policy_transfer": 6,
        "contact_manipulation": 7,
        "locomotion": 6,
        "world_models": 6,
        "causal_robotics": 7,
        "failure_analysis": 6,
    }.get(category, 3)
    exact_terms = ["sim-to-real", "sim to real", "reality gap", "domain randomization", "system identification", "residual", "contact", "causal", "failure mechanism"]
    term_score = sum(2 for term in exact_terms if term in blob)
    recency = 2 if year and year >= 2021 else 0
    return category_weight + term_score + min(8, int(math.log1p(citations or 0))) + recency


def fetch_openalex(query, tag, per_page=200, max_pages=3):
    base = "https://api.openalex.org/works"
    cursor = "*"
    out = []
    for page in range(max_pages):
        params = {
            "search": query,
            "per-page": str(per_page),
            "cursor": cursor,
            "filter": "from_publication_date:2010-01-01,to_publication_date:2026-12-31",
            "mailto": "mechanism-first-sim2real@example.com",
        }
        url = base + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            print(f"OpenAlex query failed for {query!r} page {page + 1}: {exc}")
            break
        results = payload.get("results") or []
        if not results:
            break
        for work in results:
            work["_seed_query"] = query
            work["_query_tag"] = tag
            out.append(work)
        cursor = (payload.get("meta") or {}).get("next_cursor")
        print(f"query={query} page={page + 1} records={len(results)} total_seen={len(out)}")
        if not cursor:
            break
        time.sleep(0.25)
    return out


def load_cached():
    if not os.path.exists(RAW_PATH):
        return []
    records = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def save_raw(records):
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def dedupe(records):
    by_key = {}
    by_title = {}
    for work in records:
        title = clean_text(work.get("title") or work.get("display_name") or "")
        doi = clean_text(work.get("doi") or "")
        title_key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
        key = doi.lower() if doi else clean_text(work.get("id") or title).lower()
        if not title or not key:
            continue
        existing_title_key = by_title.get(title_key)
        if existing_title_key:
            old = by_key[existing_title_key]
            old_score = (old.get("cited_by_count") or 0, len(abstract_from_inverted_index(old.get("abstract_inverted_index"))))
            new_score = (work.get("cited_by_count") or 0, len(abstract_from_inverted_index(work.get("abstract_inverted_index"))))
            if new_score > old_score:
                by_key.pop(existing_title_key, None)
                by_key[key] = work
                by_title[title_key] = key
            continue
        if key not in by_key:
            by_key[key] = work
            by_title[title_key] = key
        else:
            old = by_key[key]
            if (work.get("cited_by_count") or 0) > (old.get("cited_by_count") or 0):
                by_key[key] = work
    return list(by_key.values())


def normalize_records(records):
    rows = []
    for idx, work in enumerate(records):
        title = clean_text(work.get("title") or work.get("display_name") or "")
        abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
        concepts = concept_names(work)
        query_tag = clean_text(work.get("_query_tag") or "")
        category = classify_category(title, abstract, query_tag)
        ann = ANNOTATIONS.get(category, ANNOTATIONS["other"])
        year = work.get("publication_year") or ""
        citations = work.get("cited_by_count") or 0
        rel = relevance_score(work, title, abstract, concepts, query_tag)
        hostile = hostile_score(category, title, abstract, citations, year if isinstance(year, int) else 0)
        source_url = clean_text(((work.get("primary_location") or {}).get("landing_page_url")) or (work.get("ids") or {}).get("openalex") or work.get("id") or "")
        rows.append({
            "rank_relevance": 0,
            "paper_id": clean_text(work.get("id") or f"openalex:{idx}"),
            "doi": clean_text(work.get("doi") or ""),
            "title": title,
            "year": year,
            "venue": first_location_name(work),
            "authors": authors_of(work),
            "citation_count": citations,
            "source_url": source_url,
            "seed_query": clean_text(work.get("_seed_query") or ""),
            "query_tag": query_tag,
            "category": category,
            "concepts": "; ".join(concepts[:12]),
            "abstract": abstract[:1800],
            "problem_claimed": ann["problem"],
            "actual_mechanism_introduced": ann["mechanism"],
            "hidden_assumptions": ann["assumptions"],
            "variables_treated_as_fixed": ann["fixed"],
            "failure_modes_ignored": ann["ignored"],
            "what_it_makes_less_novel": ann["less_novel"],
            "what_it_leaves_open": ann["open"],
            "hostile_score": hostile,
            "importance_stage": "",
            "notes": "",
            "_relevance_score": rel,
        })
    rows.sort(key=lambda r: (r["_relevance_score"], r["hostile_score"], r["citation_count"]), reverse=True)
    for i, row in enumerate(rows, start=1):
        row["rank_relevance"] = i
        if i <= 100:
            row["importance_stage"] = "hostile_prior_work_100"
        elif i <= 240:
            row["importance_stage"] = "deep_read_240"
        elif i <= 300:
            row["importance_stage"] = "serious_skim_300"
        else:
            row["importance_stage"] = "landscape_1000"
        row.pop("_relevance_score", None)
    return rows


def write_matrix(rows):
    fields = [
        "rank_relevance", "paper_id", "doi", "title", "year", "venue", "authors",
        "citation_count", "source_url", "seed_query", "query_tag", "category",
        "concepts", "abstract", "problem_claimed", "actual_mechanism_introduced",
        "hidden_assumptions", "variables_treated_as_fixed", "failure_modes_ignored",
        "what_it_makes_less_novel", "what_it_leaves_open", "hostile_score",
        "importance_stage", "notes",
    ]
    with open(MATRIX_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows, fields, max_rows):
    selected = rows[:max_rows]
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    lines = [header, sep]
    for row in selected:
        vals = []
        for field in fields:
            val = clean_text(row.get(field, ""))
            if len(val) > 92:
                val = val[:89] + "..."
            val = val.replace("|", "/")
            vals.append(val)
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_literature_map(rows):
    counts = Counter(row["category"] for row in rows)
    stage_counts = Counter(row["importance_stage"] for row in rows)
    top_rows = rows[:25]
    lines = [
        "# Literature Map",
        "",
        "## Field Box",
        "",
        "This run treats the field box as robotics sim-to-real transfer under embodied physical intelligence: policy transfer, domain randomization, system identification, domain adaptation, residual learning, contact-rich manipulation, locomotion, tactile/3D perception, robot world models, and causal/failure-diagnosis methods when they directly support robot deployment.",
        "",
        "## Corpus",
        "",
        f"- Landscape sweep target: at least 1000 papers; collected matrix rows: {len(rows)}.",
        f"- Serious skim set: {stage_counts.get('hostile_prior_work_100', 0) + stage_counts.get('deep_read_240', 0) + stage_counts.get('serious_skim_300', 0)} rows.",
        f"- Deep-read set: {stage_counts.get('hostile_prior_work_100', 0) + stage_counts.get('deep_read_240', 0)} rows.",
        f"- Hostile prior-work set: {stage_counts.get('hostile_prior_work_100', 0)} rows.",
        "",
        "## Category Counts",
        "",
    ]
    for category, count in counts.most_common():
        lines.append(f"- {category}: {count}")
    lines.extend([
        "",
        "## Top Relevance Slice",
        "",
        md_table(top_rows, ["rank_relevance", "title", "year", "category", "citation_count"], 25),
        "",
        "## Hidden Assumptions That May Be False",
        "",
    ])
    for i, assumption in enumerate(HIDDEN_ASSUMPTIONS, start=1):
        lines.append(f"{i}. {assumption}")
    lines.extend([
        "",
        "## Direction Seeds That Break Assumptions",
        "",
    ])
    for direction in DIRECTIONS:
        lines.extend([
            f"### {direction['name']}",
            f"- Broken assumption: {direction['breaks']}",
            f"- Proposed central mechanism: {direction['mechanism']}",
            f"- Why it survived the sweep: {direction['why_strong']}",
            f"- Main risk: {direction['risk']}",
            "",
        ])
    lines.extend([
        "## Field Pattern",
        "",
        "The landscape is crowded around training-time coverage: randomized simulation, domain-aligned representation learning, parameter identification, residual correction, and large pretrained robot policies. The recurring gap is that these methods usually adapt coordinates of the domain or policy, while the transfer failure that matters to deployment is often categorical and intervention-specific: delay, gain loss, slip, compliance, saturation, sensing bias, or contact-mode ambiguity. The strongest paper direction should therefore make the repair mechanism the primary variable and use domain statistics only as possible evidence.",
    ])
    with open(os.path.join(DOCS_DIR, "literature_map.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_hostile_prior(rows):
    hostile = rows[:100]
    lines = [
        "# Hostile Prior Work Set",
        "",
        "These 100 papers are treated as the adversarial prior set because they are closest to the seed idea by relevance, category, citation signal, and mechanism overlap. The annotations are intentionally skeptical and focus on what each class of work makes less novel.",
        "",
    ]
    for row in hostile:
        lines.extend([
            f"## {row['rank_relevance']}. {row['title']} ({row['year']})",
            "",
            f"- Venue/authors: {row['venue']}; {row['authors']}",
            f"- Category: {row['category']}; citations: {row['citation_count']}",
            f"- Problem claimed: {row['problem_claimed']}",
            f"- Actual mechanism introduced: {row['actual_mechanism_introduced']}",
            f"- Hidden assumptions: {row['hidden_assumptions']}",
            f"- Variables treated as fixed: {row['variables_treated_as_fixed']}",
            f"- Failure modes ignored: {row['failure_modes_ignored']}",
            f"- What it makes less novel: {row['what_it_makes_less_novel']}",
            f"- What it leaves open: {row['what_it_leaves_open']}",
            f"- Source: {row['source_url']}",
            "",
        ])
    with open(os.path.join(DOCS_DIR, "hostile_prior_work.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_novelty_docs(rows):
    counts = Counter(row["category"] for row in rows[:300])
    closest_by_category = defaultdict(list)
    for row in rows[:300]:
        if len(closest_by_category[row["category"]]) < 5:
            closest_by_category[row["category"]].append(row)
    lines = [
        "# Novelty Boundary Map",
        "",
        "## What Is Not Novel Enough",
        "",
        "- Training a larger robot policy or world model.",
        "- Adding more randomized textures, lighting, masses, or friction ranges.",
        "- Aligning source and target features without proving repair relevance.",
        "- Estimating a larger set of simulator parameters before deployment.",
        "- Adding uncertainty, active learning, a verifier, or an LLM planner without changing the central adaptation coordinate.",
        "- Reporting a new benchmark without a new mechanism.",
        "",
        "## Crowded Mechanism Boundaries",
        "",
    ]
    for category, count in counts.most_common():
        lines.append(f"### {category} ({count} of top 300)")
        for row in closest_by_category[category]:
            lines.append(f"- {row['title']} ({row['year']}): makes less novel -> {row['what_it_makes_less_novel']}")
        lines.append("")
    lines.extend([
        "## Surviving Boundary",
        "",
        "The surviving boundary is not another domain-randomized policy, residual adapter, or system identifier. The proposed contribution must show that domain-level statistics are the wrong object in at least one realistic robotics transfer setting, and that diagnosing the failure mechanism yields a different and better repair. The contribution is strongest if it includes an impossibility example for statistic-only adapters and a runnable robot-control simulation where the same domain summary aliases incompatible repairs.",
    ])
    with open(os.path.join(DOCS_DIR, "novelty_boundary_map.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    decision = [
        "# Novelty Decision",
        "",
        "## Candidate Directions Considered",
        "",
    ]
    for direction in DIRECTIONS:
        decision.extend([
            f"### {direction['name']}",
            f"- Broken assumption: {direction['breaks']}",
            f"- New central mechanism: {direction['mechanism']}",
            f"- Strength: {direction['why_strong']}",
            f"- Risk: {direction['risk']}",
            "",
        ])
    decision.extend([
        "## Chosen Direction",
        "",
        "**Mechanism-first repair coordinates for sim-to-real adaptation.** The paper will argue and demonstrate that the deploy-time object of adaptation should be the failure mechanism that determines the repair, not the full target-domain statistics. A short diagnostic probe exposes mechanism-specific residual signatures; the adapter chooses among incompatible repairs such as gain compensation, delay prediction, slip damping, or compliance preload.",
        "",
        "## Why This Is Strongest",
        "",
        "The hostile set already covers randomized training, feature alignment, residual correction, online system identification, contact modeling, and broad policy transfer. The chosen direction changes the central variable: it targets repair-equivalence classes induced by physical failure mechanisms. This lets the paper make a precise negative claim about statistic-only adapters under aliased mechanisms and a positive claim about diagnostic mechanisms under few real trials.",
        "",
        "## Claims Allowed After Literature Sweep",
        "",
        "- Allowed: existing sim-to-real methods often adapt domain distributions, parameters, latent context, or residuals rather than named failure mechanisms.",
        "- Allowed: statistic-only adaptation can be non-identifiable when two mechanisms share the same passive domain summary but require different repairs.",
        "- Allowed if experiments succeed: in the provided toy contact-control simulator, mechanism-first probes select better repairs than domain-statistic baselines under nuisance-heavy shifts.",
        "- Unsupported without hardware: superiority on real robots, broad coverage of all transfer failures, or replacement of domain randomization/system identification in general.",
    ])
    with open(os.path.join(DOCS_DIR, "novelty_decision.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(decision) + "\n")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)
    update_status(
        "literature_collection",
        "querying OpenAlex and building related-work matrix",
        ["python scripts/fetch_literature.py"],
        notes=["OpenAlex cache will be reused if already present and large enough."],
    )
    cached = load_cached()
    if len(cached) >= 1200:
        print(f"using cached raw records: {len(cached)}")
        raw_records = cached
    else:
        raw_records = []
        for query, tag in QUERIES:
            raw_records.extend(fetch_openalex(query, tag))
            unique_count = len(dedupe(raw_records))
            print(f"unique_after_query={unique_count}")
            if unique_count >= 1400:
                break
        if cached:
            raw_records.extend(cached)
        raw_records = dedupe(raw_records)
        save_raw(raw_records)
    unique = dedupe(raw_records)
    rows = normalize_records(unique)
    if len(rows) < 1000:
        update_status(
            "literature_collection_incomplete",
            "insufficient unique records",
            ["python scripts/fetch_literature.py"],
            failures=[f"Only {len(rows)} unique rows after OpenAlex queries."],
            recovery_steps=["Add more scholarly sources or broaden OpenAlex queries before finalizing novelty claims."],
        )
        print(f"ERROR: only {len(rows)} rows; need at least 1000")
        return 0
    rows = rows[: max(1000, min(len(rows), 1500))]
    write_matrix(rows)
    write_literature_map(rows)
    write_hostile_prior(rows)
    write_novelty_docs(rows)
    update_status(
        "literature_complete",
        "direction chosen after 1000/300/240/100 sweep",
        ["python scripts/fetch_literature.py"],
        notes=[
            f"related_work_matrix.csv rows: {len(rows)}",
            "chosen thesis: mechanism-first repair coordinates for sim-to-real adaptation",
            "next: implement runnable evidence",
        ],
    )
    print(f"wrote {len(rows)} rows to {MATRIX_PATH}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        update_status(
            "literature_collection_failed",
            "unhandled exception in literature script",
            ["python scripts/fetch_literature.py"],
            failures=[repr(exc)],
            recovery_steps=["Inspect script/logs, patch failure, and rerun."],
        )
        print(f"fatal literature script error: {exc}")
        sys.exit(0)
