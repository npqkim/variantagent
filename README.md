# variantagent

Align short DNA reads to a reference with a hand-built FM-index, call variants,
then ground each one in ClinVar/dbSNP via an LLM agent that retrieves clinical
significance instead of inventing it.

## Status
- [x] Phase 1: FM-index core (suffix array, BWT, C array, Occ, backward search)
- [ ] Phase 2: read mapping
- [ ] Phase 3: variant caller -> VCF
- [ ] Phase 4: eval against injected truth set
- [ ] Phase 5: agent (tool-grounded interpretation)
- [ ] Phase 6: package (CLI/API, Docker)

## Run
    python -m pytest -q
    python phase1_demo.py