import os
import requests
from pathlib import Path
from tqdm import tqdm

# Base URL for NCBI Datasets API (v2alpha)
NCBI_BASE = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha"

def fetch_bacterial_metadata(query="bacteria", max_records=1000):
    """
    Fetch genome accessions for bacterial isolates from NCBI based on a query term.

    Parameters:
        query (str): The search term for organisms (e.g., "Halomonas", "Salinibacter").
        max_records (int): Maximum number of records to retrieve.

    Returns:
        List of genome accession numbers (strings).
    """
    url = f"{NCBI_BASE}/genome/accession"

    # Query parameters for filtering results
    params = {
        "filters.organism": query,               # Organism search filter
        "page_size": 500,                        # Max records per request (API limit)
        "filters.host": "environmental sample",  # Optional: get environmental isolates
        "filters.assembly_level": "complete",    # High-quality assemblies only
    }

    all_accessions = []
    headers = {"Accept": "application/json"}

    # Loop through paginated API results
    for i in range(0, max_records, 500):
        params["page_token"] = str(i)  # Set pagination token
        r = requests.get(url, params=params, headers=headers)

        # Handle API errors
        if r.status_code != 200:
            raise Exception(f"Error fetching metadata: {r.text}")

        # Parse JSON response
        chunk = r.json()
        accessions = chunk.get("accessions", [])
        all_accessions.extend(accessions)

        # Stop if no further pages
        if "next_page_token" not in chunk:
            break

    return all_accessions


def download_genomes(accessions, output_dir="data/raw/genomes"):
    """
    Download genome assemblies from NCBI using the datasets CLI.

    Parameters:
        accessions (list): List of genome accession numbers (e.g., GCF_000009605.1)
        output_dir (str): Folder where downloaded .zip files will be saved.
    """
    # Ensure output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Download each genome with `datasets` CLI tool
    for acc in tqdm(accessions, desc="Downloading genomes"):
        # Build command to download only the genome sequence (not annotation or protein)
        cmd = f"datasets download genome accession {acc} --include genome --filename {output_dir}/{acc}.zip"
        os.system(cmd)  # Run command in shell (could replace with subprocess for more safety)
