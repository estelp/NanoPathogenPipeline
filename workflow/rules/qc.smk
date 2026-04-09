import os

# Recursive search for FASTQ files
fastq_files = []
for root, dirs, files in os.walk(config['input_dir']):
    for f in files:
        if f.endswith(".fastq") or f.endswith(".fastq.gz"):
            if config['pattern'].replace("*","") in f:
                fastq_files.append(os.path.join(root, f))

# Sample names
SAMPLES = [os.path.basename(f).split(".fastq")[0].replace(".gz","") for f in fastq_files]

rule all:
    input:
        expand(os.path.join(RUN_DIR, "{sample}", "QC"), sample=SAMPLES)

rule qc:
    input:
        fq=lambda wildcards: next(f for f in fastq_files if wildcards.sample in f)
    output:
        qc_dir=lambda wildcards: os.path.join(RUN_DIR, wildcards.sample, "QC")
    threads: config['threads']
    conda: "../../envs/qc.yaml"
    shell:
        """
        mkdir -p {output.qc_dir}
        NanoPlot -t {threads} --fastq {input.fq} -o {output.qc_dir}
        """
