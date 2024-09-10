# Sherlock eval

Inspired by an [episode of the Dwarkesh Podcast](https://x.com/dwarkesh_sp/status/1825931761118794102), this is an eval that tests LLMs ability to determine the culprit in Sherlock Holmes murder mysteries. 

![Model Performance](data/visualizations/model_performance.png)

Each mystery
- Has multiple suspects, and one culprit.
- Classified as either `easy`, `medium` or `hard` with respect to difficulty. Difficulty is determined by multiple factors, see the [make_story.ipynb](https://github.com/patrickmziet/sherlock/blob/main/make_story.ipynb) notebook for more.
- In the figure below, the dotted red lines show 

The dotted red lines show the performance of choosing a suspect at random for `easy`, `medium` and `hard`. For example `gpt-4o-2024-05-13` performs much better than random for easy mysteries, 66.7% vs 30.6%. 

At the moment, a lot of models fail to even output an acceptable answer, resulting in 0%, see `claude-3-haiku-20240307`. This is a problem that possible requires better prompting.

|                            |   easy |   medium |   hard |   Average |
|:---------------------------|-------:|---------:|-------:|----------:|
| claude-3-5-sonnet-20240620 |   33.3 |     66.7 |   66.7 |      55.6 |
| claude-3-opus-20240229     |   33.3 |     33.3 |   33.3 |      33.3 |
| gpt-4-turbo-2024-04-09     |   33.3 |     33.3 |   33.3 |      33.3 |
| claude-3-sonnet-20240229   |   66.7 |      0.0 |    0.0 |      22.2 |
| gpt-4o-2024-05-13          |   66.7 |      0.0 |    0.0 |      22.2 |
| gpt-4-0613                 |   33.3 |     33.3 |    0.0 |      22.2 |
| Random                     |   30.6 |     13.7 |    8.6 |      17.6 |
| gpt-4o-mini-2024-07-18     |    0.0 |      0.0 |    0.0 |       0.0 |
| claude-3-haiku-20240307    |    0.0 |      0.0 |    0.0 |       0.0 |
## Contributing a mystery

The aim is to have mysteries contributed from other people, please fork the repo, make a new story and submit it as a PR. 

Follow the instructions in the [make_story.ipynb](https://github.com/patrickmziet/sherlock/blob/main/make_story.ipynb) notebook. 

Have a look at the existing stories in [data/mysteries](https://github.com/patrickmziet/sherlock/tree/main/data/mysteries).