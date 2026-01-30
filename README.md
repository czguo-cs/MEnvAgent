# MEnvAgent

<!-- <p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Conference-ICML%202026-blue"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-green.svg"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-orange.svg"></a>
</p> -->

<p align="center">
  <a href="https://arxiv.org/abs/XXXX.XXXXX"><img src="https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg"></a>
  <a href="https://huggingface.co/datasets/ernie-research/MEnvBench"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HF-MEnvBench-yellow"></a>
  <a href="https://huggingface.co/datasets/ernie-research/MEnvData-SWE"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HF-MEnvData--SWE-orange"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-green.svg"></a>
</p>

**MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering**

Official implementation of MEnvAgent, an automated framework for constructing executable environments across 10 programming languages to enable scalable generation of verifiable software engineering data.

<!-- TODO: Convert PDF to SVG before release (recommended) or PNG
<p align="center">
  <img src="assets/MEnvAgent-intro.svg" alt="MEnvAgent Overview" width="800"/>
</p>
<p align="center">
  <em>Comparison between manual environment construction and MEnvAgent's automated approach</em>
</p>
-->

## 📰 News

<!-- * **[Jan. 2026]**: Our paper "MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering" has been submitted to ! -->
* **[Jan. 2026]**: We release MEnvData-SWE, the largest open-source polyglot dataset of realistic verifiable Docker environments to date, comprising **3,005 task instances** from **942 repositories** across **10 programming languages**.
* **[Jan. 2026]**: MEnvBench is now available - an execution-based environment construction benchmark with rigorous quality assurance, covering **1,000 tasks** across **10 programming languages** from diverse domains.

## ⭐ Key Features

- **Multi-Language Support**: Automated environment construction for 10 mainstream programming languages (Python, Java, TypeScript, JavaScript, Rust, Go, C++, Ruby, PHP, C)
- **Multi-Agent Architecture**: Planning-Execution-Verification closed-loop system with specialized agents for different tasks
- **Environment Reuse Mechanism**: Novel approach that reduces overhead by incrementally patching retrieved environments instead of building from scratch
- **Docker/Kubernetes Backend**: Flexible container orchestration supporting both Docker and Kubernetes
- **Fail2Pass Validation**: Rigorous validation ensuring tests fail before fix and pass after applying patches
- **High Performance**: Achieves 8.6% improvement in F2P rates while reducing time costs by 43% compared to baselines

## 🏗️ Architecture Overview

MEnvAgent employs a multi-agent system structured into three iterative stages:

<p align="center">
  <img src="assets/MEnvAgent-main.png" alt="MEnvAgent Architecture" width="100%"/>
</p>
<p align="center">
  <em>Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments. (Bottom) Planning-Execution-Verification loop with autonomous agents.</em>
</p>

### 📝 Planning Stage
- **Repository Analysis Agent**: Explores repository structure and generates comprehensive summary
- **Environment Setup Agent**: Determines suitable base image and generates installation scripts
- **Test Configuration Agent**: Synthesizes compatible test configuration scripts

### ⚡ Execution Stage
- **Environment Execution Agent**: Instantiates containers and executes build commands with real-time monitoring
- Dynamic error resolution and automatic retry mechanisms

### ✅ Verification Stage
- **Verification Agent**: Executes tests and performs error attribution
- Iterative refinement loop with diagnostic feedback to planning stage

### ♻️ Environment Reuse Mechanism
Instead of building environments from scratch, MEnvAgent:
1. Retrieves similar historical environments from the Environment Pool
2. Uses **EnvPatchAgent** to generate incremental patches
3. Applies patches to adapt the retrieved environment to target requirements
4. Significantly reduces computational overhead and improves success rates

## 📋 Prerequisites

- Python 3.10+
- Docker (version 27.0.3+ recommended)
- Kubernetes (optional, for K8s backend)
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/MEnvAgent.git
cd MEnvAgent
```

### 2. Set Up Python Environment

```bash
conda create --name menvagent python=3.10 -y
conda activate menvagent
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Set your LLM API configuration
export OPENAI_API_BASE_URL=<your_base_url>
export OPENAI_KEY=<your_api_key>

# (Optional) Configure proxy settings if needed
export http_proxy="http://your-proxy:port"
export https_proxy="http://your-proxy:port"
export no_proxy="localhost,127.0.0.1"
```

## 📊 MEnvBench: Evaluation Benchmark

MEnvBench is a comprehensive benchmark for evaluating multi-language environment building and test execution:

- **Coverage**: 1,000 tasks across 10 mainstream programming languages
- **Repositories**: 200 diverse open-source repositories
- **Diversity**: Multi-dimensional sampling ensuring high coverage across domains, popularity, and complexity

### 📈 Evaluation Results

Performance comparison with state-of-the-art baselines:

| Model | F2P Rate (%) | Time (min) | Cost (USD) |
|-------|--------------|------------|------------|
| **MEnvAgent** | **TBD** | **TBD** | **TBD** |
| Baseline-1 | TBD | TBD | TBD |
| Baseline-2 | TBD | TBD | TBD |

*Note: Detailed results will be added from paper*

### 🎯 Key Improvements
- **8.6%** improvement in Fail-to-Pass (F2P) rates
- **43%** reduction in time costs
- Consistent performance across all 10 supported languages

## 💾 MEnvData Dataset

We release **MEnvData**, a high-quality polyglot SWE dataset with **2K Docker images** and **3K agent trajectories**:

- **2K Docker Images**: Pre-built environment images with verified dependencies
- **3K Agent Trajectories**: Complete execution trajectories for training and analysis
- **Multi-Language**: Coverage across 10 mainstream programming languages
- **Verified Quality**: All instances include executable environments with validation
- **Format**: Compatible with SWE-Bench evaluation framework

### 🔗 Dataset Access

🤗 **Hugging Face Dataset**: [https://huggingface.co/datasets/TODO/MEnvData](https://huggingface.co/datasets/TODO/MEnvData)

```python
# Load the dataset using Hugging Face datasets library
from datasets import load_dataset

dataset = load_dataset("TODO/MEnvData")
```

### 📋 Dataset Structure

Each instance contains:
- Repository information (org, repo, commit)
- Test patches and fix patches
- Docker base image configurations
- Verified test execution scripts
- Agent interaction trajectories

*Note: Dataset will be publicly released upon paper publication*


### Running Fail2Pass Validation

```bash
python evaluation/run_evaluation.py \
  --dataset_name "output/results.json" \
  --predictions_path "gold" \
  --max_workers 5 \
  --run_id "fail2pass_check" \
  --output_path "run_instances" \
  --timeout 3600 \
  --is_judge_fail2pass
```

### Customizing Agent Behavior

Agents are located in `app/agents/`. Each agent can be customized by:
1. Modifying agent prompts and logic
2. Adjusting retry strategies and timeouts
3. Extending tool capabilities

## ⚙️ Configuration

### Backend Selection

```python
# Docker backend
runtime = await Runtime.create(backend="docker", docker_image="ubuntu:latest")

# Kubernetes backend
runtime = await Runtime.create(backend="kubernetes", docker_image="image:tag")
```

## 📖 Citation

If MEnvAgent helps your research or projects, please cite our paper:

```bibtex
@article{menvagent2026,
  title={MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering},
  author={TODO: Add authors from paper},
  year={2026}
}
```

## 🙏 Acknowledgements

MEnvAgent builds upon foundational work in software engineering and LLM agents:
- **[SWE-Bench-Live](https://github.com/microsoft/SWE-bench-Live)**: A dynamic, continuously-updated benchmark for evaluating language models on real-world software tasks with fresh, uncontaminated GitHub issues
- **[SWE-Factory](https://arxiv.org/abs/2506.10954)**: Automated factory for GitHub Issue Resolution Training Data and Evaluation Benchmarks.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions, issues, or collaborations, please:
- Open an issue on GitHub
- Contact: czguo@ir.hit.edu.cn

---
