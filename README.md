# Political Inclination

This repository implements the Political Inclination Analysis Tool, supporting both **Persian** and **Nepali** languages. It extends the research presented in [SIGUL 2024](https://aclanthology.org/2024.sigul-1.49), exploring political and economic biases in language models trained on under-resourced languages. The tool applies various NLP techniques to assess political leanings across multiple language models.

## Directory Structure

- **`code/`**: Contains Jupyter notebooks for performing political inclination analysis.
  - **`nepali/`**: Analysis for Nepali text using language models.
  - **`persian/`**: Analysis for Persian text using BERT models.
  
- **`responses/`**: Stores model outputs in JSONL format.
  - **`nepali/`**: Results from fill-mask and generative models for Nepali.
  - **`persian/`**: Results from fill-mask and generative models for Persian.
  
- **`results/`**: Visualization and text score outputs in charts and text format.
  - **`nepali/`**: Output charts and scores for Nepali models.
  - **`persian/`**: Output charts and scores for Persian models.
  
- **`scores/`**: Detailed model score files in text format for both languages.
  - **`nepali/`**: Scores for various fill-mask and generative models for Nepali.
  - **`persian/`**: Scores for various fill-mask and generative models for Persian.

- **`converter.py`**: Script to convert raw outputs into a specific format for further processing.

- **`score-plotter.py`**: Utility to generate visual score plots.

## Citation

If you use this tool, please cite:

```bibtex
@inproceedings{barkhordar-etal-2024-unexpected,
    title = "Why the Unexpected? Dissecting the Political and Economic Bias in {P}ersian Small and Large Language Models",
    author = "Barkhordar, Ehsan  and Thapa, Surendrabikram  and Maratha, Ashwarya  and Naseem, Usman",
    booktitle = "Proceedings of the 3rd Annual Meeting of the Special Interest Group on Under-resourced Languages @ LREC-COLING 2024",
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.sigul-1.49",
    pages = "410--420"
}
```
