#!/usr/bin/env python3
"""Post-process pandoc LaTeX output for neutrosophic tensor paper.

Fixes:
1. Section hierarchy (promote one level)
2. Remove hypertargets
3. Fix figure paths
4. Fix \textgreater{}/\textless{} artifacts
5. Split into section files
"""

import re
from pathlib import Path

RAW = Path(__file__).parent / "paper_raw.tex"
OUT = Path(__file__).parent


def process():
    raw = RAW.read_text()

    # Extract body
    body_match = re.search(
        r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL
    )
    body = body_match.group(1).strip()

    # Remove hypertargets
    body = re.sub(r"\\hypertarget\{[^}]*\}\{\s*%?\n?", "", body)

    # Fix multi-line section titles
    body = re.sub(
        r"(\\(?:sub)*section\{[^}]*)\n\s*([^}]*\})",
        r"\1 \2",
        body,
    )

    # Remove stray labels
    body = re.sub(r"\\label\{[^}]*\}", "", body)

    # Fix stray closing braces from hypertarget removal
    body = re.sub(r"(\\(?:sub)*section\{[^}]+)\}\}", r"\1}", body)
    body = re.sub(r"\n\s*\}\s*\n", "\n", body)

    # Remove title (it's in main.tex now)
    body = re.sub(
        r"\\section\{From Scalars to Tensors[^}]*\}\s*", "", body
    )

    # Remove author block from body (it's in main.tex)
    body = re.sub(
        r"Tony Mason.*?²Anthropic \(AI research collaborator\)\s*",
        "",
        body,
        flags=re.DOTALL,
    )

    # Promote section hierarchy
    # \subsection{N. Title} → \section{Title}
    body = re.sub(
        r"\\subsection\{(\d+\.\s+)([^}]+)\}",
        lambda m: f"\\section{{{m.group(2)}}}",
        body,
    )
    # \subsubsection{N.N Title} → \subsection{Title}
    body = re.sub(
        r"\\subsubsection\{(\d+\.\d+\s+)([^}]+)\}",
        lambda m: f"\\subsection{{{m.group(2)}}}",
        body,
    )
    # Abstract stays as \subsection → \section
    body = re.sub(r"\\subsection\{Abstract\}", r"\\begin{abstract}", body)

    # Appendix sections
    body = re.sub(
        r"\\subsection\{(Appendix [^}]+)\}",
        r"\\section{\1}",
        body,
    )
    # Remaining \subsubsection → \subsection
    body = re.sub(
        r"\\subsubsection\{([^}]+)\}",
        r"\\subsection{\1}",
        body,
    )

    # Second pass: fix stray }}
    body = re.sub(
        r"(\\(?:sub)*section\{[^}]+)\}\}", r"\1}", body
    )

    # Fix figure paths (point to local copies)
    body = body.replace("../results/", "")

    # Fix \textgreater{} and \textless{} → > and <
    body = body.replace("\\textgreater{}", ">")
    body = body.replace("\\textless{}", "<")

    # Fix Unicode characters not in Latin Modern
    body = body.replace("\u2082", "$_{2}$")  # subscript 2
    body = body.replace("\u2248", "$\\approx$")  # approximately equal
    body = body.replace("\u00b7", "$\\cdot$")  # middle dot

    # Close abstract (find end of abstract paragraph)
    # Abstract runs until the next \section
    abstract_start = body.find("\\begin{abstract}")
    if abstract_start >= 0:
        next_section = body.find("\\section{", abstract_start + 1)
        if next_section >= 0:
            body = (
                body[:next_section]
                + "\\end{abstract}\n\n"
                + body[next_section:]
            )

    # Split into sections
    parts = re.split(r"(?=\\section\{)", body)
    abstract_text = parts[0].strip()

    file_map = {
        "Introduction": "introduction.tex",
        "Cross-Vendor Replication": "replication.tex",
        "The Absorption Problem": "absorption.tex",
        "Strategy 4": "tensor.tex",
        "Discussion": "discussion.tex",
        "Conclusion": "conclusion.tex",
    }

    appendix_parts = []

    for part in parts[1:]:
        title_match = re.match(r"\\section\{([^}]+)\}", part)
        if not title_match:
            continue
        title = title_match.group(1).strip()

        matched = False
        for key, fname in file_map.items():
            if key in title:
                OUT.joinpath(fname).write_text(part.strip() + "\n")
                print(f"  {fname}: {len(part.strip().splitlines())} lines")
                matched = True
                break

        if not matched:
            if "Appendix" in title:
                appendix_parts.append(part.strip())
            else:
                print(f"  UNMAPPED: '{title}'")

    OUT.joinpath("abstract.tex").write_text(abstract_text + "\n")
    print(f"  abstract.tex: {len(abstract_text.splitlines())} lines")

    if appendix_parts:
        content = "\n\n".join(appendix_parts)
        OUT.joinpath("appendix.tex").write_text(content + "\n")
        print(
            f"  appendix.tex: {len(content.splitlines())} lines"
            f" — {len(appendix_parts)} appendices"
        )

    print("\nDone.")


if __name__ == "__main__":
    process()
