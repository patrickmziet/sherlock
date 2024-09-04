# Sherlock eval

Inspired by an [episode of the Dwarkesh Podcast](https://x.com/dwarkesh_sp/status/1825931761118794102), this is an eval that tests LLMs ability to determine the culprit in Sherlock Holmes murder mysteries. 

## Contributing a mystery

The aim is to have mysteries contributed from other people, please fork the repo, make a new story and submit it as a PR. 

Follow the instructions in the [make_story.ipynb](https://github.com/patrickmziet/sherlock/blob/main/make_story.ipynb) notebook. 

Have a look at the existing stories in [data/mysteries](https://github.com/patrickmziet/sherlock/tree/main/data/mysteries).

## TODO
- [X] Make enter story function
- [X] Test openai model
- [X] Make plotting code
- [X] Add claude API
- [X] Write serializers
- [ ] Fix stream animation if there are no logprobs, and add green box to other plot ylabel.
- [ ] Add other plot/table functions: Performance (%) vs model, add random classifier, function to print TeX table, calibration plot
- [ ] Improve API request answer format. Give an example. Add option to "Think step by step..."
- [ ] Make at least 20 stories in each difficulty category
- [ ] Add other models
- [ ] Update README/repo landing page. Must have key figs, tables summaries etc
- [ ] Make .tex/.pdf report