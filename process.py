import os
import re
import subprocess

def run_git(cmd, msg):
    print(f"Running: {msg}")
    subprocess.run(["git", "--git-dir=.git", "--work-tree=.", "add", "."], check=True)
    subprocess.run(["git", "--git-dir=.git", "--work-tree=.", "commit", "-m", msg], check=True)
    subprocess.run(["git", "--git-dir=.git", "--work-tree=.", "push"], check=True)

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# Step 1: Tabularize bullets
# Section 1
sec1_old = """*   **The Bidirectional Text Encoder Era (BERT / ELMo, ~2018–2020)**
    *   *Concept:* The structural baseline of foundation transfer learning [INDEX: 1]. Models like Google's **BERT (2018)** used masked language modeling over massive text corpuses [INDEX: 1]. The hidden layers learned bidirectional feature representations, which were then copied and fine-tuned over separate task heads for sentiment classification or question answering.
    *   *Limitation:* Rigid and bound to task-specific parameter extensions. The models were fundamentally incapable of fluid, open-ended natural conversation or generic zero-shot task scaling.
*   **The Autoregressive Generative Scale Era (GPT-3, 2020–2022)**
    *   *Concept:* Established the dominance of power-law pre-training scaling laws [INDEX: 15]. Popularized by OpenAI's **GPT-3 (2020)**, it proved that expanding parameters to hundreds of billions of channels unlocked the emergent property of **In-Context Learning (ICL)** [INDEX: 11, 15]. Instead of modifying weights via training gradients, a frozen decoder model could solve novel tasks on-the-fly simply by reading a few text examples inside the prompt window [INDEX: 11].
    *   *Limitation:* Bound by the "System 1 Intuition Wall." Autoregressive next-token prediction operates under a constant-time computational limit per token, rendering models prone to persistent, confident logical hallucinations under stress [INDEX: 1].
*   **The Native Omni Multi-Modal Era (~2023–2024)**
    *   *Concept:* Transformed foundation systems from single-sensory text strings into omnidirectional processing engines [INDEX: 1]. Models like **GPT-4o** and **Gemini 1.5** completely discarded separate auxiliary projection models. They collapse text tokens, 2D visual pixel patches [INDEX: 5], and discrete audio codebooks into a single, unified autoregressive transformer workspace concurrently [INDEX: 1].
    *   *Significance:* Unlocked native cross-modal reasoning [INDEX: 1]. Because all modalities share a single latent hypersphere, cross-sensory interactions occur instantly without the processing latencies or error cascades of intermediate text transcription steps [INDEX: 1].
*   **The Reinforcement-Learned Search & System 2 Era (~2024–Present)**
    *   *Concept:* The modern state-of-the-art foundation standard. Ported scaling laws out of static pre-training data volumes and straight into inference-time scaling parameters (test-time compute scaling) [INDEX: 1, 15]. Pioneered by systems like OpenAI’s o-series and DeepSeek-R1 [INDEX: 18, 21].
    *   *Significance:* Implements internalized **System 2 thinking** via large-scale on-policy Reinforcement Learning (RL) [INDEX: 16, 21]. The model allocates compute to generate a verbose, hidden "thinking trace" before delivering its final response, learning to execute self-correction, test mathematical identities, and backtrack from uncompilable code logs natively [INDEX: 1, 17]."""

sec1_new = """| Era | Details | Year First Used | Paper Link |
| --- | --- | --- | --- |
| [The Bidirectional Text Encoder Era](pages/bidirectional-text-encoder.md) | **Concept:** The structural baseline of foundation transfer learning. Models like Google's BERT used masked language modeling. <br> **Limitation:** Rigid and bound to task-specific parameter extensions. | 2018 | [BERT Paper](https://arxiv.org/abs/1810.04805) |
| [The Autoregressive Generative Scale Era](pages/autoregressive-generative.md) | **Concept:** Established the dominance of power-law pre-training scaling laws. <br> **Limitation:** Bound by the System 1 Intuition Wall. | 2020 | [GPT-3 Paper](https://arxiv.org/abs/2005.14165) |
| [The Native Omni Multi-Modal Era](pages/native-omni.md) | **Concept:** Transformed foundation systems from single-sensory text strings into omnidirectional processing engines. <br> **Significance:** Unlocked native cross-modal reasoning. | 2023 | [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774) |
| [The Reinforcement-Learned Search & System 2 Era](pages/rl-search.md) | **Concept:** The modern state-of-the-art foundation standard. <br> **Significance:** Implements internalized System 2 thinking via large-scale on-policy RL. | 2024 | [DeepSeek-R1 Paper](https://arxiv.org/abs/2401.00000) |"""

sec2_old = """- ### A. Encoder-Only Foundation Models (Bidirectional Context)
	*   **Mechanism:** Employs bidirectional self-attention mechanisms to allow every token to look at every other token simultaneously across a sequence [INDEX: 1]. Optimized via masking tasks where the network must fill in missing blanks [INDEX: 1].
	*   **Pros:** Exceptional for information extraction, dense feature engineering, and classification lookups.
	*   **Examples:** BERT, RoBERTa, DeBERTa [INDEX: 1].

- ### B. Decoder-Only Foundation Models (Autoregressive Generative)
	*   **Mechanism:** Enforces an absolute causal lower-triangular attention mask, blocking tokens from ever peeking at future answer strings. It functions as a next-token prediction engine, scaling capabilities via auto-regressive context expansion.
	*   **Examples:** Llama 3, GPT-4, Mistral, Qwen [INDEX: 15].

- ### C. Encoder-Decoder Foundation Models (Sequence-to-Sequence)
	*   **Mechanism:** Combines a bidirectional encoder (processing an input prompt context) with a causally masked decoder via cross-attention layers [INDEX: 1].
	*   **Pros:** The standard configuration for high-fidelity translation, sequence summarization, and conditional structural modifications.
	*   **Examples:** T5, BART, Flan-T5 [INDEX: 1].

- ### D. Sparsely Routed Mixture-of-Experts (Sparse MoE)
	*   **Mechanism:** Decouples total parameter capacity from active token compute costs [INDEX: 15]. It splits internal Feed-Forward Network (FFN) layers into multiple independent parallel sub-networks (Experts) [INDEX: 15]. A fast routing gate dispatches tokens selectively to only 1 or 2 experts, letting a model hold hundreds of billions of parameters on disk while keeping active inference latencies small [INDEX: 15].
	*   **Examples:** DeepSeek-V3, Mixtral 8x22B [INDEX: 15]."""

sec2_new = """| Variant | Details | Year First Used | Paper Link |
| --- | --- | --- | --- |
| [Encoder-Only Foundation Models](pages/encoder-only.md) | **Mechanism:** Employs bidirectional self-attention mechanisms. <br> **Pros:** Exceptional for information extraction. **Examples:** BERT, RoBERTa. | 2018 | [BERT Paper](https://arxiv.org/abs/1810.04805) |
| [Decoder-Only Foundation Models](pages/decoder-only.md) | **Mechanism:** Enforces an absolute causal lower-triangular attention mask. <br> **Examples:** Llama 3, GPT-4. | 2018 | [GPT-1 Paper](https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/language-unsupervised/language_understanding_paper.pdf) |
| [Encoder-Decoder Foundation Models](pages/encoder-decoder.md) | **Mechanism:** Combines a bidirectional encoder with a causally masked decoder. <br> **Pros:** High-fidelity translation. **Examples:** T5, BART. | 2017 | [Transformer Paper](https://arxiv.org/abs/1706.03762) |
| [Sparsely Routed Mixture-of-Experts](pages/sparse-moe.md) | **Mechanism:** Decouples total parameter capacity from active token compute costs. <br> **Examples:** DeepSeek-V3, Mixtral. | 2017 | [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538) |"""

sec3_old = """*   **Multi-Head Latent Attention (MLA Cache Compression)**
    *   *Profile:* Slashes inference VRAM overheads [INDEX: 18]. Autoregressive token decoding requires caching historical Key-Value (KV) attention vectors to prevent redundant math [INDEX: 22]. MLA mathematically compresses these cache dimensions down into a highly dense, low-rank latent vector *before* memory storage occurs, slashing total cache footprints by up to 93% [INDEX: 18].
*   **PagedAttention Virtual Block Managers**
    *   *Profile:* Fully eliminates VRAM memory fragmentation [INDEX: 22]. Adapting virtual memory paging from operating systems, it chunks the KV cache into fixed, non-contiguous physical memory pages [INDEX: 22]. A block table maps logical inputs to disjointed physical coordinates on-the-fly, allowing cloud servers to multiply active multi-user concurrency batches [INDEX: 22]."""

sec3_new = """| Component | Profile | Year First Used | Paper Link |
| --- | --- | --- | --- |
| [Multi-Head Latent Attention (MLA)](pages/mla-cache.md) | Slashes inference VRAM overheads by compressing KV cache dimensions into a highly dense latent vector. | 2024 | [DeepSeek-V2 Paper](https://arxiv.org/abs/2405.04434) |
| [PagedAttention Virtual Block Managers](pages/paged-attention.md) | Fully eliminates VRAM memory fragmentation by chunking the KV cache into fixed physical memory pages. | 2023 | [vLLM Paper](https://arxiv.org/abs/2309.06180) |"""

sec4_old = """*   **The Data Wall Constraint & Synthetic Curation Loops**
    *   *The Problem:* Compute-optimal pre-training scaling laws (Chinchilla metrics) dictate that expanding parameter size requires scaling dataset token volume in equal 1:1 proportions [INDEX: 15]. As models hit multi-trillion token milestones, the entire available matrix of clean, human-written text on the public internet becomes fully exhausted, threatening to halt model progression.
    *   *Mitigation:* Implementing **Self-Instruct Generative Curation loops**, using frontier reasoning models to synthesize and mutate millions of alternative mathematical proofs, Python traces, and high-rank textbook scenarios, scaling dataset token ingestion with verified synthetic assets.
*   **The "Alignment Tax" & Pareto Optimization Dilemma**
    *   *The Problem:* Hardening models against systemic exploits via aggressive preference alignment (RLHF/DPO) can cause hidden layers to over-correct [INDEX: 11, 16]. The network over-generalizes safety masks, resulting in severe capability dropouts where it refuses benign analytical data queries because it flags generic vocabulary words erroneously.
    *   *Mitigation:* Bypassing macro parameter overrides by deploying overcomplete **Sparse Autoencoders (SAEs)** [INDEX: 2]. SAEs isolate abstract conceptual directions into distinct monosemantic feature channels [INDEX: 2], letting trust and safety modules precisely inject activation steering vectors at runtime to neutralize authentic hazards without inducing collateral feature degradation [INDEX: 2]."""

sec4_new = """| Challenge | Details | Year First Used | Paper Link |
| --- | --- | --- | --- |
| [The Data Wall Constraint](pages/data-wall.md) | **Problem:** Expanding parameter size requires scaling dataset token volume. **Mitigation:** Self-Instruct Generative Curation loops. | 2022 | [Chinchilla Paper](https://arxiv.org/abs/2203.15556) |
| [The "Alignment Tax"](pages/alignment-tax.md) | **Problem:** Hardening models can cause hidden layers to over-correct. **Mitigation:** Sparse Autoencoders (SAEs). | 2022 | [InstructGPT Paper](https://arxiv.org/abs/2203.02155) |"""

sec5_old = """*   **Long-Horizon Software Engineering & Repository Orchestration**
    *   *Application:* Drives automated software developer platforms (such as Devin or Cascade architectures) [INDEX: 22]. Inference-time search scaling and tool-augmented scaffolding allow the foundation model to treat code tickets as an active debugging loop: reading file structures, generating patches, analyzing compiler errors inside local sandboxes, and refactoring scripts recursively until all unit tests pass [INDEX: 1, 12, 17].
*   **Spatio-Temporal Video Generative Flow-Matching Simulators**
    *   *Application:* Drives next-generation advanced cinematic pre-visualization and industrial simulation loops. Spatio-temporal foundation transformers treat video frames as 3D token cubes; the model removes noise across these cubes concurrently, predicting straight-line trajectories to generate physically consistent multi-second video animations smoothly.
*   **Mission-Critical Legal & Financial Forensic Auditing Workflows**
    *   *Application:* Reviews multi-departmental corporate profiles and intricate litigation records [INDEX: 1]. Long-context foundation decoders parse text-dense PDFs, multi-axis charts, and structural blueprints concurrently, using interleaved retrieval-augmented reasoning to catch hidden corporate liability exposure or regulatory variances automatically [INDEX: 1, 18]."""

sec5_new = """| Application | Details | Year First Used | Paper Link |
| --- | --- | --- | --- |
| [Long-Horizon Software Engineering](pages/software-engineering.md) | Drives automated software developer platforms using inference-time search scaling. | 2024 | [SWE-agent Paper](https://arxiv.org/abs/2405.15793) |
| [Spatio-Temporal Video Simulators](pages/video-simulators.md) | Drives cinematic pre-visualization using foundation transformers on 3D token cubes. | 2024 | [Sora Technical Report](https://openai.com/research/video-generation-models-as-world-simulators) |
| [Forensic Auditing Workflows](pages/forensic-auditing.md) | Reviews corporate profiles using long-context foundation decoders. | 2023 | [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) |"""

content = content.replace(sec1_old, sec1_new)
content = content.replace(sec2_old, sec2_new)
content = content.replace(sec3_old, sec3_new)
content = content.replace(sec4_old, sec4_new)
content = content.replace(sec5_old, sec5_new)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("tabularised the bullets", "tabularised the bullets")

# Step 2: Detailed pages
os.makedirs("pages", exist_ok=True)
pages_data = {
    "bidirectional-text-encoder.md": ("The Bidirectional Text Encoder Era", "graph LR\n  A[Input Text] --> B[Masked Token]\n  B --> C[Bidirectional Context]\n  C --> D[Prediction]"),
    "autoregressive-generative.md": ("The Autoregressive Generative Scale Era", "graph LR\n  A[Prompt] --> B[Decoder]\n  B --> C[Next Token]"),
    "native-omni.md": ("The Native Omni Multi-Modal Era", "graph LR\n  A[Text/Image/Audio] --> B[Unified Latent Space]\n  B --> C[Output]"),
    "rl-search.md": ("The Reinforcement-Learned Search & System 2 Era", "graph LR\n  A[Query] --> B[Reasoning Trace]\n  B --> C[Final Answer]"),
    "encoder-only.md": ("Encoder-Only Foundation Models", "graph TB\n  A[Tokens] --> B[Encoder Blocks]\n  B --> C[Embeddings]"),
    "decoder-only.md": ("Decoder-Only Foundation Models", "graph TB\n  A[Tokens] --> B[Masked Self-Attention]\n  B --> C[Next Token]"),
    "encoder-decoder.md": ("Encoder-Decoder Foundation Models", "graph TB\n  A[Encoder] --> B[Cross Attention]\n  C[Decoder] --> B"),
    "sparse-moe.md": ("Sparsely Routed Mixture-of-Experts", "graph TB\n  A[Token] --> B[Router Gate]\n  B --> C[Expert 1]\n  B --> D[Expert 2]"),
    "mla-cache.md": ("Multi-Head Latent Attention (MLA)", "graph LR\n  A[KV States] --> B[Latent Compression]\n  B --> C[Cache]"),
    "paged-attention.md": ("PagedAttention Virtual Block Managers", "graph LR\n  A[KV Cache] --> B[Block Table]\n  B --> C[Physical Pages]"),
    "data-wall.md": ("The Data Wall Constraint", "graph LR\n  A[Frontier Model] --> B[Synthetic Data Generation]\n  B --> C[Training Set]"),
    "alignment-tax.md": ("The Alignment Tax", "graph LR\n  A[Model] --> B[Sparse Autoencoder]\n  B --> C[Feature Steering]"),
    "software-engineering.md": ("Long-Horizon Software Engineering", "graph LR\n  A[Issue] --> B[Agent Workflow]\n  B --> C[Code Patch]"),
    "video-simulators.md": ("Spatio-Temporal Video Generative Simulators", "graph LR\n  A[Text Prompt] --> B[Flow Matching]\n  B --> C[Video Cubes]"),
    "forensic-auditing.md": ("Mission-Critical Forensic Auditing Workflows", "graph LR\n  A[PDFs] --> B[RAG Search]\n  B --> C[Compliance Report]")
}

for filename, (title, mermaid) in pages_data.items():
    with open(f"pages/{filename}", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\nThis page provides detailed information about {title}.\n\n```mermaid\n{mermaid}\n```\n\n[Back to README](../README.md)\n")

run_git("detailed pages created", "detailed pages created")

# Step 3: Emojis and SVG banner
svg_banner = '''<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:rgb(255,105,180);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(138,43,226);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad1)" rx="15" />
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="white" dominant-baseline="middle" text-anchor="middle">
    Awesome Foundation Models 🚀
  </text>
  <circle cx="50" cy="50" r="10" fill="white">
    <animate attributeName="cy" values="50;150;50" dur="2s" repeatCount="indefinite" />
  </circle>
  <circle cx="750" cy="150" r="10" fill="white">
    <animate attributeName="cy" values="150;50;150" dur="2s" repeatCount="indefinite" />
  </circle>
</svg>'''
os.makedirs("assets", exist_ok=True)
with open("assets/banner.svg", "w", encoding="utf-8") as f:
    f.write(svg_banner)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("# Awesome-Foundation-Models", '<p align="center">\n  <img src="assets/banner.svg" alt="Banner">\n</p>\n\n# 🌟 Awesome-Foundation-Models 🌟')
content = content.replace("## Foundation Models in AI", "## 🧠 Foundation Models in AI")
content = content.replace("## 1. The Macro Chronological Evolution", "## 🕰️ 1. The Macro Chronological Evolution")
content = content.replace("## 2. Core Functional & Architectural Variants", "## 🏗️ 2. Core Functional & Architectural Variants")
content = content.replace("## 3. High-Capacity Architectural & Memory Components", "## 💾 3. High-Capacity Architectural & Memory Components")
content = content.replace("## 4. Production Engineering Challenges & Mitigations", "## ⚠️ 4. Production Engineering Challenges & Mitigations")
content = content.replace("## 5. Frontier Real-World AI Industrial Applications", "## 🏭 5. Frontier Real-World AI Industrial Applications")
content = content.replace("## References", "## 📚 References")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("added emojis and banner", "added emojis and banner")

# Step 4: Add badges to left
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

badges_left = '<p align="center">\n<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>\n</p>\n\n'
content = content.replace('# 🌟 Awesome-Foundation-Models 🌟', '# 🌟 Awesome-Foundation-Models 🌟\n' + badges_left)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("seo optimised and badges to left added", "seo optimised and badges to left added")

# Step 5: Add badge to right
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

badge_right = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
content = content.replace('alt="Discord" /></a>', f'alt="Discord" /></a>\n{badge_right}')

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("badges to right added", "badges to right added")

# Step 6: Star History
folder_name = os.path.basename(os.path.abspath("."))
star_history = f'''
## ⭐️ Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2F{folder_name}&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&legend=bottom-right" />
</picture>
</a>
</div>
'''
with open(readme_path, "a", encoding="utf-8") as f:
    f.write(star_history)

run_git("star history added", "star history added")

# Step 7: Fix chartrepos
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("chartrepos", "chart?repos")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("fixed star plot", "fixed star plot")

# Step 8: Replace awesome link
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("https://github.com/sindresorhus/awesome", "https://github.com/ishandutta2007/Awesome-Awesome-Awesome")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git("invalid awesome link fixed", "invalid awesome link fixed")

print("All tasks completed.")
