#!/usr/bin/env bash
JOB_NAME="snakemake_master_process."$(date --iso-8601='minutes')
LOG_DIR=logs/
MEMORY=8000

mkdir -p $LOG_DIR

bsub -R "select[mem>$MEMORY] rusage[mem=$MEMORY] span[hosts=1]" \
    -M "$MEMORY" \
    -o "$LOG_DIR"/"$JOB_NAME".o \
    -e "$LOG_DIR"/"$JOB_NAME".e \
    -J "$JOB_NAME" \
      snakemake -p "$@"

exit 0
