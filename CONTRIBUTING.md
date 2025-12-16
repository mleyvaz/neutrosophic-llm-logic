# Contributing to Neutrosophic Logic for LLMs

Thank you for your interest in contributing to this research project! We welcome contributions from researchers, developers, and enthusiasts interested in Neutrosophic Logic and Large Language Models.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs. actual behavior
- Your environment (Python version, OS, etc.)

### Submitting Pull Requests

1. **Fork the repository** and create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, descriptive commits
   ```bash
   git commit -m "Add feature: description of changes"
   ```

3. **Write or update tests** to cover your changes
   ```bash
   pytest tests/ -v
   ```

4. **Follow the code style** using Black and Flake8
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

5. **Update documentation** if needed (README.md, docstrings, etc.)

6. **Push to your fork** and open a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/neutrosophic-llm-logic.git
cd neutrosophic-llm-logic

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Code Standards

- **Python Version:** 3.11+
- **Style Guide:** PEP 8 (enforced with Black and Flake8)
- **Documentation:** NumPy-style docstrings
- **Testing:** pytest with >80% coverage target

### Example Docstring

```python
def analyze_neutrosophic_components(truth, indeterminacy, falsity):
    """
    Analyze the neutrosophic components of a reasoning task.
    
    Parameters
    ----------
    truth : float
        The degree of truth [0, 1].
    indeterminacy : float
        The degree of indeterminacy [0, 1].
    falsity : float
        The degree of falsity [0, 1].
    
    Returns
    -------
    dict
        Analysis results including sum, hyper-truth status, and interpretation.
    """
```

## Research Contributions

If you're contributing research findings or novel analyses:

1. **Ensure reproducibility:** Include code, data, and detailed methodology
2. **Cite sources:** Use APA format for all citations
3. **Document assumptions:** Clearly state any assumptions or limitations
4. **Provide visualizations:** Include figures and tables to support findings

## Areas for Contribution

- **Code improvements:** Optimization, refactoring, new features
- **Documentation:** Clarifications, examples, tutorials
- **Testing:** Unit tests, integration tests, edge cases
- **Analysis:** New experiments, comparative studies, extensions
- **Visualization:** Improved plots, interactive dashboards
- **Multimodal extension:** Application to vision, audio, or other modalities

## Communication

- **GitHub Issues:** For bug reports and feature requests
- **Pull Requests:** For code contributions with discussion
- **Email:** For research collaboration inquiries

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

---

Thank you for contributing to advancing research in Neutrosophic Logic and Large Language Models!
