# Image quality test for higher resolutions

This repo contains the code to reproduce the images used for the lab and online test for image quality.
The overall idea is to evaluate H.265 for image compression and compare the lab and online test results (for more details see the reference listed in the Acknowledgments section).

## Structure

* images: source images and sampling procedure
* pre_analysis: pre analysis of the images, including some image quality models
* test_1: analysis of the lab test
* test_2: analysis of the online/crowd test

## Requirements
To run the evaluation scripts you need python3 with:
  * jupyter, pandas, seaborn, numpy, scipy and scikit-learn


## Acknowledgments
If you use this software in your research, please include a link to the repository and reference the following paper.

```bibtex
@article{goeringrao2023crowd,
  title={Quality Assessment of Higher Resolution Images and Videos with Remote Testing},
  author={Steve G\"oring and Rakesh {Rao Ramachandra Rao} and Alexander Raake},
  journal={Quality and User Experience (QUEX)},
  year={2023}
}
```

## License
GNU General Public License v3. See [LICENSE.md](LICENSE.md) file in this repository.

