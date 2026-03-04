import zipfile
import tempfile
import shutil
from pathlib import Path

REQUIRED_FILES = {
    "profile": "Profile.csv",
    "positions": "Positions.csv",
    "education": "Education.csv",
    "skills": "Skills.csv",
}

OPTIONAL_FILES = {
    "recommendations": "Recommendations_Received.csv",
}


def extract(zip_path: str) -> tuple[Path, dict[str, Path]]:
    """
    Extract a LinkedIn data export ZIP and locate relevant CSV files.

    Returns:
        (temp_dir, files) where files maps file type -> Path
        Caller is responsible for cleanup via cleanup(temp_dir).
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"Not a valid ZIP file: {zip_path}")

    temp_dir = Path(tempfile.mkdtemp(prefix="linkedin_"))

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(temp_dir)

    # Case-insensitive lookup of all extracted CSVs
    all_files = {f.name.lower(): f for f in temp_dir.rglob("*.csv")}

    found = {}

    for key, filename in REQUIRED_FILES.items():
        match = all_files.get(filename.lower())
        if match is None:
            raise FileNotFoundError(f"Required file not found in ZIP: {filename}")
        found[key] = match

    for key, filename in OPTIONAL_FILES.items():
        match = all_files.get(filename.lower())
        if match:
            found[key] = match

    return temp_dir, found


def cleanup(temp_dir: Path) -> None:
    """Remove the temporary extraction directory."""
    shutil.rmtree(temp_dir, ignore_errors=True)
