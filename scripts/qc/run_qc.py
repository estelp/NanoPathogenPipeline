#!/usr/bin/env python3

import argparse
import os
import glob
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def run_command(cmd):
    """Run a shell command and log it."""
    logging.info(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Quality Control of Nanopore FASTQ files using NanoPlot"
    )

    parser.add_argument(
        "-i", "--input_dir",
        required=True,
        help="Parent directory containing FASTQ files (searches recursively)"
    )
    parser.add_argument(
        "-o", "--output_parent",
        required=True,
        help="Parent directory for all runs (the script will create a timestamped subfolder)"
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=4,
        help="Number of threads for NanoPlot"
    )
    parser.add_argument(
        "-p", "--pattern",
        default="*_barcode*.fastq*",
        help="Pattern to select FASTQ files (default '*_barcode*.fastq*')"
    )

    args = parser.parse_args()

    # Create a timestamped run directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_dir = os.path.join(args.output_parent, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    logging.info(f"Run output directory created: {run_dir}")

    # Search for all FASTQ files recursively using glob
    fastq_files = glob.glob(os.path.join(args.input_dir, '**', args.pattern), recursive=True)

    if not fastq_files:
        logging.error(f"No FASTQ files found in {args.input_dir} matching pattern {args.pattern}")
        return

    logging.info(f"Found {len(fastq_files)} FASTQ files.")

    # Loop over each FASTQ file
    for fq in fastq_files:
        # Get the base filename without path and extension
        base_name = os.path.basename(fq).split(".fastq")[0]

        # Create a directory for this sample
        sample_dir = os.path.join(run_dir, base_name)
        qc_dir = os.path.join(sample_dir, "QC")
        os.makedirs(qc_dir, exist_ok=True)

        # Build the NanoPlot command
        cmd = f"NanoPlot -t {args.threads} --fastq {fq} -o {qc_dir}"
        run_command(cmd)

        logging.info(f"QC finished for {fq} -> {qc_dir}")


if __name__ == "__main__":
    main()
