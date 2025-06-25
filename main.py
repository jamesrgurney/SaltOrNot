# main.py
import salinity_classifier.downloader as dl
print(">> Using module from:", dl.__file__)


from salinity_classifier.downloader import fetch_bacterial_metadata, download_genomes

# Call the new CLI-based metadata fetcher
accessions = fetch_bacterial_metadata(query="Halomonas", max_records=10)

print(f"Found {len(accessions)} genomes:")
for acc in accessions:
    print(f" - {acc}")

# Download genomes to disk
download_genomes(accessions[:3])  # Download just the first 3 for now
