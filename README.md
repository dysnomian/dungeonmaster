# Dungeonmaster

An attempt to teach an LLM to be a storyteller for story-first pen and paper RPG, a la Powered By The Apocalypse or Forged in the Dark.

## Requirements

Python >= 3.10
Docker

## Installation

```shell
git clone git@github.com:dysnomian/dungeonmaster.git && cd dungeonmaster
docker build -f Dockerfile -t dungeonmaster_dev_img .
docker run -it -v $(pwd)/autogen:/app dungeonmaster_dev_img
```

[Colab notebook](https://colab.research.google.com/github/dysnomian/dungeonmaster/blob/main/notebooks/Colab-TextGen-GPU.ipynb)

## Planning
[Github project](https://github.com/users/dysnomian/projects/2)

## Further Reading
