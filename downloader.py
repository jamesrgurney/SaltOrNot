# downloader.py

import os
import json
import subprocess
from pathlib import Path
from tqdm import tqdm

def fetch_bacterial_metadata(query="Halomonas", max_records=10):
    """
    Fetch genome accessions using the NCBI `datasets` command-line tool
    based on a taxonomic query (e.g. "Halomonas").

    Parameters:
        query (str): Taxon or organism name to search for.
        max_records (int): Number of accessions to return.

    Returns:
        List of accession strings (e.g. GCF_000009605.1).
    """
    print("✅ Running CLI version of fetch_bacterial_metadata")

    # This uses the CLI, not requests!
    cmd = [
        "datasets", "summary", "genome", "taxon", query,
        "--limit", str(max_records),
        "--as-json-lines"
    ]

    try:
        # Run datasets CLI command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to fetch metadata using CLI: {e.stderr}")

    accessions = []

    # Parse output: each line is a JSON object
    for line in result.stdout.strip().split("\n"):
        if line.strip():  # skip blanks
            entry = json.loads(line)
            acc = entry.get("accession")
            if acc:
                accessions.append(acc)

    return accessions


def download_genomes(accessions, output_dir="data/raw/genomes"):
    """
    Download genome assemblies using the `datasets` CLI tool.

    Parameters:
        accessions (list): List of genome accessions to download.
        output_dir (str): Directory where downloaded .zip files will be stored.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for acc in tqdm(accessions, desc="📥 Downloading genomes"):
        cmd = [
            "datasets", "download", "genome", "accession", acc,
            "--include", "genome",
            "--filename", str(output_dir / f"{acc}.zip")
        ]
        subprocess.run(cmd)
